from __future__ import print_function

import collections  # Imported to support ordered dictionaries in Python
import contextlib

try:
    import cStringIO
except ImportError:
    import io as cStringIO

import random
import sys

import requests.exceptions

import wikipedia  # Provides and API-like functionality to search and access Wikipedia data
import wikipedia.exceptions
from nltk.corpus import wordnet as wn  # WordNet
from nltk.corpus.reader.wordnet import WordNetError


class Engine():
    def __init__(self, nlp):
        self.nlp = nlp  # Load en_core_web_sm, English, 50 MB, default model
        self.entity_map = {
            'WHO': ['PERSON'],
            'WHAT': ['PERSON', 'NORP', 'FACILITY', 'ORG', 'GPE', 'LOC', 'PRODUCT', 'EVENT', 'WORK_OF_ART', 'LANGUAGE', 'DATE', 'TIME', 'PERCENT', 'MONEY', 'QUANTITY', 'ORDINAL', 'CARDINAL'],
            'WHEN': ['DATE', 'TIME', 'EVENT'],
            'WHERE': ['FACILITY', 'GPE', 'LOC']
        }  # Map wh question words to entity categories
        self.coefficient = {'frequency': 0.36, 'precedence': 0.13, 'proximity': 0.21, 'mention': 0.30}  # Coefficients for scoring

    # Entry function for this class. Dragonfire calls only this function. Unlike Learner.respond() it executes TTS because of its late reponse nature.
    def respond(self, com, tts_output=False, userin=None, user_prefix=None, is_server=False):
        result = None
        subject, subjects, focus, subject_with_objects = self.semantic_extractor(com)  # Extract the subject, focus, objects etc.
        if not subject:
            return False

        doc = self.nlp(com)  # spaCy does all kinds of NLP analysis in one function
        query = subject  # Wikipedia search query (same as the subject)
        # This is where the real search begins
        if query:  # If there is a Wikipedia query determined
            if not tts_output and not is_server: print("Please wait...")
            if tts_output and not is_server: userin.say("Please wait...", True, False)  # Gain a few more seconds by saying Please wait...
            wh_question = []
            for word in doc:  # Iterate over the words in the command(user's speech)
                if word.tag_ in ['WDT', 'WP', 'WP$', 'WRB']:  # if there is a wh word then
                    wh_question.append(word.text.upper())  # append it by converting to uppercase
            if not wh_question:
                return False
            with nostderr():
                try:
                    wikiresult = wikipedia.search(query)  # run a Wikipedia search with the query
                    if len(wikiresult) == 0:  # if there are no results
                        result = "Sorry, " + user_prefix + ". But I couldn't find anything about " + query + " in Wikipedia."
                        if not tts_output and not is_server: print(result)
                        if tts_output and not is_server: userin.say(result)
                        return result
                    wikipedia.page(wikiresult[0])
                except requests.exceptions.ConnectionError:  # if there is a connection error
                    result = "Sorry, " + user_prefix + ". But I'm unable to connect to Wikipedia servers."
                    if not is_server:
                        userin.execute([" "], "Wikipedia connection error.")
                        if not tts_output: print(result)
                        if tts_output: userin.say(result)
                    return result
                except wikipedia.exceptions.DisambiguationError as disambiguation:  # if there is a disambiguation
                    wikiresult = wikipedia.search(disambiguation.options[0])  # run Wikipedia search again with the most common option
                except:
                    result = "Sorry, " + user_prefix + ". But something went horribly wrong while I'm searching Wikipedia."
                    if not tts_output and not is_server: print(result)
                    if tts_output and not is_server: userin.say(result)
                    return result
            findings = []  # empty findings list for scoring
            nth_page = 0  # nth Wikipedia page/article
            while not findings:  # while there are no any findings
                if not len(wikiresult) >= (nth_page + 1):  # prevent index error
                    break
                with nostderr():
                    try:
                        wikipage = wikipedia.page(wikiresult[nth_page])  # Get the next Wikipedia page/article from the search results (this line also handles the search at the same time)
                    except requests.exceptions.ConnectionError:  # if there is a connection error
                        result = "Sorry, " + user_prefix + ". But I'm unable to connect to Wikipedia servers."
                        if not is_server:
                            userin.execute([" "], "Wikipedia connection error.")
                            if not tts_output: print(result)
                            if tts_output: userin.say(result)
                        return result
                    except:
                        result = "Sorry, " + user_prefix + ". But something went horribly wrong while I'm searching Wikipedia."
                        if not tts_output and not is_server: print(result)
                        if tts_output and not is_server: userin.say(result)
                        return result
                nth_page += 1  # increase the visited page/article count
                if nth_page > 5: break  # if script searched more than 5 Wikipedia pages/articles then give up
                wikidoc = self.nlp(wikipage.content)  # parse the Wikipedia page/article content using spaCy NLP library
                sentences = [sent.string.strip() for sent in wikidoc.sents]  # each individual sentence in the current Wikipedia page/article
                # return [' '.join(subjects),' '.join(pobjects)]
                all_entities = []  # all entities, useful or not all of them
                mention = {}  # sentences with focus mentioned
                subject_entities_by_wordnet = None  # target entities according to the subject
                if 'WHAT' in wh_question:  # if it's a WHAT question then
                    subject_entities_by_wordnet = self.wordnet_entity_determiner(subject_with_objects, tts_output, is_server, userin, user_prefix)  # result of wordnet_entity_determiner()
                    if not subject_entities_by_wordnet:
                        return True
                for sentence in reversed(sentences):  # iterate over the sentences (in reversed order)
                    sentence = self.nlp(sentence)  # parse the sentence using spaCy NLP library
                    for ent in sentence.ents:  # iterate over the all entities in the sentence (has been found by spaCy)
                        all_entities.append(ent.text)  # append the entity to all_entities
                        mention[ent. text] = 0.0  # the value if focus not even defined or the focus is NOT even mentioned
                        for wh in wh_question:  # iterate over the all wh questions have been found in the Command(user's speech)
                            if wh.upper() in self.entity_map:  # if the wh question is defined in entity_map (on top) then
                                target_entities = self.entity_map[wh.upper()]  # get the target entities from the entity_map
                                if wh.upper() == 'WHAT':  # if the question is WHAT then
                                    target_entities = []  # empty the target entities because we will replace them with the result of wordnet_entity_determiner()
                                    for subject_entity_by_wordnet in subject_entities_by_wordnet:  # for each entity in subject_entities_by_wordnet
                                        target_entities.append(subject_entity_by_wordnet)  # append the entity to target entities
                                if ent.label_ in target_entities:  # if entity label is in target entities listed then
                                    findings.append(ent.text)  # WE FOUND! a possible entity so append the text to findings
                                    if focus:  # if focus is defined then
                                        if focus in sentence.text:  # if focus is in the sentence then
                                            mention[ent. text] += 1.0 * sentence.text.count(focus)  # assign the how many times the entity mentioned in the sentence

            if findings:  # if there is a finding or there are findings then

                frequency = collections.Counter(findings)  # count the occurrences of the exacty same finding and return a unique dictionary. High frequency means high score
                max_freq = max(frequency.values())  # max occurrence
                for key, value in frequency.items():  # iterate over the unique dictionary
                    frequency[key] = float(value) / max_freq  # divide the occurence by max occurence to find the real frequency value

                precedence = {}  # precedence according to the location of the finding in the Wikipedia article. Closer to the top, greater the score is
                unique = list(set(findings))  # unique the findings list
                for i in range(len(unique)):  # iterate over that unqiue list
                    precedence[unique[i]] = float(len(unique) - i) / len(unique)  # calculate the score

                proximity = {}  # proximity to the subject. Closer to the subject (in terms of location), greater the score is
                subject_indices = []  # index values of subject occurrences
                for i in range(len(all_entities)):  # iterate over the all entities
                    for subject in subjects:  # iterate over the all subjects
                        for word in subject.split():  # iterate over the each word in the subject
                            if word in all_entities[i]:  # if the word is in all entities then
                                subject_indices.append(i)  # append the index
                for i in range(len(all_entities)):  # iterate over the all entities, again
                    for index in subject_indices:  # for each index
                        inverse_distance = float((len(all_entities) - 1) - abs(i - index)) / (len(all_entities) - 1)  # calculate the proximity of the entity to the subject
                        if all_entities[i] in proximity:  # if the entity is already appended then
                            proximity[all_entities[i]] = (proximity[all_entities[i]] + inverse_distance) / 2  # assign the proximity by calculating the average
                        else:
                            proximity[all_entities[i]] = inverse_distance  # otherwise assign the proximity directly
                    if all_entities[i] not in proximity:  # if it's somehow not appended then
                        proximity[all_entities[i]] = 0  # give it a zero score

                ranked = {}  # the eventual ranking/scoring
                for key, value in frequency.items():  # iterate over the all findings (frequency, precedence, proximity, mention all of them holds all findings)
                    if key not in query:  # eliminate the findings that already inside of the Wikipedia query
                        ranked[key] = (value * self.coefficient['frequency'] + precedence[key] * self.coefficient['precedence'] + proximity[key] * self.coefficient['proximity'] + mention[key] * self.coefficient['mention'])  # calculate the absolute score

                result = sorted(ranked.items(), key=lambda x: x[1])[::-1][0][0]
                if not tts_output and not is_server: print(sorted(ranked.items(), key=lambda x: x[1])[::-1][:5])  # if not tts_output print the best 5 result
                if tts_output and not is_server: userin.say(result, True, True)  # if tts_output say the best result (via TTS obviously)
                return result  # also return the best result
            else:  # if no any findings
                return False  # in case of no any findings return False

    # function to determine the entity of the subject
    def wordnet_entity_determiner(self, subject, tts_output, is_server, userin=None, user_prefix=None):
        entity_samples_map = {
            'PERSON': ['person', 'character', 'human', 'individual', 'name'],
            'NORP': ['nationality', 'religion', 'politics'],
            'FACILITY': ['building', 'airport', 'highway', 'bridge', 'port'],
            'ORG': ['company', 'agency', 'institution', 'university'],
            'GPE': ['country', 'city', 'state', 'address', 'capital'],
            'LOC': ['geography', 'mountain', 'ocean', 'river'],
            'PRODUCT': ['product', 'object', 'vehicle', 'food'],
            'EVENT': ['hurricane', 'battle', 'war', 'sport'],
            'WORK_OF_ART': ['art', 'book', 'song', 'painting'],
            'LANGUAGE': ['language', 'accent', 'dialect', 'speech'],
            'DATE': ['year', 'month', 'day'],
            'TIME': ['time', 'hour', 'minute'],
            'PERCENT': ['percent', 'rate', 'ratio', 'fee'],
            'MONEY': ['money', 'cash', 'salary', 'wealth'],
            'QUANTITY':
            ['measurement', 'amount', 'distance', 'height', 'population'],
            'ORDINAL': ['ordinal', 'first', 'second', 'third'],
            'CARDINAL': ['cardinal', 'number', 'amount', 'mathematics']
        }  # entity samples to use it in WordNet similarity
        doc = self.nlp(subject)  # spaCy does all kinds of NLP analysis in one function
        subject = []  # empty list to hold the nouns in the subject string
        for word in doc:  # for each word in the subject string
            # if word.pos_ not in ['PUNCT','SYM','X','CONJ','DET','ADP','SPACE']:
            if word.pos_ == 'NOUN':  # if word is a noun then
                subject.append(word.text.lower())  # convert it to lowercase and append it
        entity_scores = {}  # empty dictionary to hold entity scores
        for entity, samples in entity_samples_map.items():  # iterate over the entity_samples_map
            entity_scores[entity] = 0  # initial score of the entity is 0
            for sample in samples:  # for each sample in the samples
                sample_wn = wn.synset(sample + '.n.01')  # convert the sample to a WordNet noun
                for word in subject:  # for each word in the subject
                    try:
                        word_wn = wn.synset(word + '.n.01')  # convert the word to a WodNet noun
                        entity_scores[entity] += word_wn.path_similarity(sample_wn)  # calculate the similarity using WordNet path_similarity() and add it to the score of the entity
                    except WordNetError:
                        if not is_server:
                            message = "Sorry, " + user_prefix + ". But I'm unable to understand the word '" + word + "'."
                            userin.execute([" "], "NLP(WordNet) error. Unrecognized word: " + word)
                            if not tts_output: print(message)
                            if tts_output: userin.say(message)
                            return False
            entity_scores[entity] = entity_scores[entity] / len(samples)  # to calculate the average; divide the total by the amount of samples
        if not tts_output and not is_server: print(sorted(entity_scores.items(), key=lambda x: x[1])[::-1][:3])  # if not tts_output print the best 3 result
        result = sorted(entity_scores.items(), key=lambda x: x[1])[::-1][0][0]  # assign the best result
        if result == 'FACILITY': return [result, 'ORG']  # currently, spaCy is incorrectly classifying many entities that belongs to FACILITY as ORG. Because of that include ORG to the return
        if result == 'PRODUCT': return [result, 'ORG']  # currently, spaCy is incorrectly classifying many entities that belongs to PRODUCT as ORG. Because of that include ORG to the return
        return [result]  # if there is no exception on above lines then return only one result but in an array. For example ['PERSON']

    # this function is only for TESTING purposes. It randomzes the coefficients so that we are able optimize the values
    def randomize_coefficients(self):
        coeff1 = round(random.uniform(0.00, 0.98), 2)
        coeff2 = round(random.uniform(0.00, (1 - coeff1)), 2)
        coeff3 = round(random.uniform(0.00, (1 - (coeff1 + coeff2))), 2)
        coeff4 = 1 - (coeff1 + coeff2 + coeff3)
        self.coefficient = {'frequency': coeff1, 'precedence': coeff2, 'proximity': coeff3, 'mention': coeff4}

    # function to clean unnecessary words from the given phrase/string. (Punctuation mark, symbol, unknown, conjunction, determiner, subordinating or preposition and space)
    def phrase_cleaner(self, phrase):
        clean_phrase = []
        for word in self.nlp(phrase):
            if word.pos_ not in ['PUNCT', 'SYM', 'X', 'CONJ', 'DET', 'ADP', 'SPACE']:
                clean_phrase.append(word.text)
        return ' '.join(clean_phrase)

    # this function extracts subject, subjects, focus, subject_with_objects
    def semantic_extractor(self, string):
        doc = self.nlp(string)  # spaCy does all kinds of NLP analysis in one function
        the_subject = None  # Wikipedia search query variable definition (the subject)
        # Followings are lists because it could be multiple of them in a string. Multiple objects or subjects...
        subjects = []  # subject list
        pobjects = []  # object of a preposition list
        dobjects = []  # direct object list
        # https://nlp.stanford.edu/software/dependencies_manual.pdf - Hierarchy of typed dependencies
        for np in doc.noun_chunks:  # Iterate over the noun phrases(chunks)
            # print(np.text, np.root.text, np.root.dep_, np.root.head.text)
            if (np.root.dep_ == 'nsubj' or np.root.dep_ == 'nsubjpass') and np.root.tag_ != 'WP':  # if it's a nsubj(nominal subject) or nsubjpass(passive nominal subject) then
                subjects.append(np.text)  # append it to subjects
            if np.root.dep_ == 'pobj':  # if it's an object of a preposition then
                pobjects.append(np.text)  # append it to pobjects
            if np.root.dep_ == 'dobj':  # if it's a direct object then
                dobjects.append(np.text)  # append it to direct objects

        # This block determines the Wikipedia query (the subject) by relying on this priority: [Object of a preposition] > [Subject] > [Direct object]
        pobjects = [x for x in pobjects]
        subjects = [x for x in subjects]
        dobjects = [x for x in dobjects]
        if pobjects:
            the_subject = ' '.join(pobjects)
        elif subjects:
            the_subject = ' '.join(subjects)
        elif dobjects:
            the_subject = ' '.join(dobjects)
        else:
            return None, None, None, None

        # This block determines the focus(objective/goal) by relying on this priority: [Direct object] > [Subject] > [Object of a preposition]
        focus = None
        if dobjects:
            focus = self.phrase_cleaner(' '.join(dobjects))
        elif subjects:
            focus = self.phrase_cleaner(' '.join(subjects))
        elif pobjects:
            focus = self.phrase_cleaner(' '.join(pobjects))
        if focus in the_subject:
            focus = None

        # Full string of all subjects and objects concatenated
        subject_with_objects = []
        for dobject in dobjects:
            subject_with_objects.append(dobject)
        for subject in subjects:
            subject_with_objects.append(subject)
        for pobject in pobjects:
            subject_with_objects.append(pobject)
        subject_with_objects = ' '.join(subject_with_objects)

        wh_found = False
        for word in doc:  # iterate over the each word in the given command(user's speech)
            if word.tag_ in ['WDT', 'WP', 'WP$', 'WRB']:  # check if there is a "wh-" question (we are determining that if it's a question or not, so only accepting questions with "wh-" form)
                wh_found = True
        if not wh_found:
            return None, None, None, None

        return the_subject, subjects, focus, subject_with_objects


@contextlib.contextmanager
def nostdout():
    save_stdout = sys.stdout
    sys.stdout = cStringIO.StringIO()
    yield
    sys.stdout = save_stdout


@contextlib.contextmanager
def nostderr():
    save_stderr = sys.stderr
    sys.stderr = cStringIO.StringIO()
    yield
    sys.stderr = save_stderr


if __name__ == "__main__":
    # TESTS
    import spacy
    EngineObj = Engine(spacy.load('en'))
    best_score = 0
    best_coefficient = None
    i = 0
    while True:
        i += 1
        print("Counter: " + str(i))
        score = 0
        EngineObj.randomize_coefficients()
        print(EngineObj.coefficient)

        # New York City
        print("\nWhere is the Times Square")
        if EngineObj.respond("Where is the Times Square") == "New York City": score += 1

        # 2,720 ft - QUANTITY
        print("\nWhat is the height of Burj Khalifa")
        if EngineObj.respond("What is the height of Burj Khalifa") == "(2,717 feet": score += 1

        # Dubai
        print("\nWhere is Burj Khalifa")
        if EngineObj.respond("Where is Burj Khalifa") == "Dubai": score += 1

        # 481 feet - QUANTITY
        print("\nWhat is the height of Great Pyramid of Giza")
        if EngineObj.respond("What is the height of Great Pyramid of Giza") == "(481 feet": score += 1

        # Kit Harington
        print("\nWho is playing Jon Snow in Game of Thrones")
        if EngineObj.respond("Who is playing Jon Snow in Game of Thrones") == "Kit Harington": score += 1

        # 8 - CARDINAL
        print("\nWhat is the atomic number of oxygen")
        if EngineObj.respond("What is the atomic number of oxygen") == "8": score += 1

        # 1.371 billion - QUANTITY
        # print "\nWhat is the population of China"
        # if EngineObj.respond("What is the population of China") == "1.371 billion": score += 1

        # Japanese - LANGUAGE
        print("\nWhat is the official language of Japan")
        if EngineObj.respond("What is the official language of Japan") == "Japanese": score += 1

        # Stark - PERSON
        print("\nWhat is the real name of Iron Man")
        if EngineObj.respond("What is the real name of Iron Man") in ["Stark", "Tony Stark"]: score += 1

        # Mehmed The Conqueror - PERSON
        print("\nWho is the conqueror of Constantinople")
        if EngineObj.respond("Who is the conqueror of Constantinople") in ["Mehmed II", "Mehmet II", "Mehmet"]: score += 1

        # 1453 - DATE TIME
        print("\nWhen Constantinople was conquered")
        if EngineObj.respond("When Constantinople was conquered") == "1453": score += 1

        # Ankara - GPE
        print("\nWhat is the capital of Turkey")
        if EngineObj.respond("What is the capital of Turkey") == "Ankara": score += 1

        # Istanbul - GPE
        print("\nWhat is the largest city of Turkey")
        if EngineObj.respond("What is the largest city of Turkey") == "Istanbul": score += 1

        # Hinduism - NORP
        # print "\nWhat is the name of the oldest religion"
        # if EngineObj.respond("What is the name of the oldest religion") == "Hinduism": score += 1

        # Hartsfield Jackson Atlanta International Airport - FACILITY
        # print "\nWhat is the name of the world's busiest airport"
        # if (EngineObj.respond("What is the name of the world's busiest airport") == "Hartsfield Jackson Atlanta International Airport"): score += 1

        # Harvard University - ORG
        print("\nWhat is the name of the world's best university")
        if EngineObj.respond("What is the name of the world's best university") in ["Harvard", "Peking University"]: score += 1

        # Nile river - LOC
        print("\nWhat is the name of the world's longest river")
        if EngineObj.respond("What is the name of the world's longest river") in ["Nile", "Amazon"]: score += 1

        # Rolls-Royce - PRODUCT
        print("\nWhat is the brand of the world's most expensive car")
        if EngineObj.respond("What is the brand of the world's most expensive car") == "Rolls-Royce": score += 1

        # World War II - EVENT
        print("\nWhat is the bloodiest war in human history")
        if EngineObj.respond("What is the bloodiest war in human history") in ["World War II", "World War I"]: score += 1

        # Da Vinci Code - WORK_OF_ART
        print("\nWhat is the name of the best seller book")
        if EngineObj.respond("What is the name of the best seller book") in ["Real Marriage", "'Real Marriage' on"]: score += 1

        # the Mariana Trench - LOC
        print("\nWhat is the lowest point in the ocean")
        if EngineObj.respond("What is the lowest point in the ocean") == "the Mariana Trench": score += 1

        # Einstein - PERSON
        print("\nWho invented General Relativity")
        if EngineObj.respond("Who invented General Relativity") == "Einstein": score += 1

        # 1945 - DATE TIME
        print("\nWhen was United Nations formed")
        if EngineObj.respond("When was United Nations formed") == "1945": score += 1

        # purpose of this block is finding the optimum value for coefficients
        if score > best_score:
            print("\n--- !!! NEW BEST !!! ---")
            best_score = score
            best_coefficient = EngineObj.coefficient
            print(str(best_score) + ' / 20')
            print(best_coefficient)
            print("------------------------\n")
