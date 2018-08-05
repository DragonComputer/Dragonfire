#!/usr/bin/python3
# -*- coding: utf-8 -*-

"""
.. module:: omniscient
    :platform: Unix
    :synopsis: the top-level submodule of Dragonfire that contains the classes related to **Omniscient**: Dragonfire's Factoid Question Answering Engine.

.. moduleauthor:: Mehmet Mert Yıldıran <mert.yildiran@bil.omu.edu.tr>
"""

import collections  # Imported to support ordered dictionaries in Python
from random import uniform  # Generate pseudo-random numbers

from dragonfire.utilities import nostderr  # With statement to suppress errors

import requests.exceptions  # HTTP for Humans
import wikipedia  # Provides and API-like functionality to search and access Wikipedia data
import wikipedia.exceptions  # Exceptions of wikipedia library
from nltk.corpus import wordnet as wn  # The WordNet corpus
from nltk.corpus.reader.wordnet import WordNetError  # To catch the errors


class Omniscient():
    """Class to provide the factoid question answering ability.
    """

    def __init__(self, nlp):
        """Initialization method of :class:`dragonfire.omniscient.Omniscient` class.

        Args:
            nlp:  :mod:`spacy` model instance.
        """

        self.nlp = nlp  # Load en_core_web_sm, English, 50 MB, default model
        self.entity_map = {
            'WHO': ['PERSON'],
            'WHAT': ['PERSON', 'NORP', 'FACILITY', 'ORG', 'GPE', 'LOC', 'PRODUCT', 'EVENT', 'WORK_OF_ART', 'LANGUAGE', 'DATE', 'TIME', 'PERCENT', 'MONEY', 'QUANTITY', 'ORDINAL', 'CARDINAL'],
            'WHEN': ['DATE', 'TIME', 'EVENT'],
            'WHERE': ['FACILITY', 'GPE', 'LOC']
        }  # Map wh question words to entity categories
        self.coefficient = {'frequency': 0.36, 'precedence': 0.13, 'proximity': 0.21, 'mention': 0.30}  # Coefficients for scoring

    def respond(self, com, tts_output=False, userin=None, user_prefix=None, is_server=False):
        """Method to respond the user's input/command using factoid question answering ability.

        Args:
            com (str):  User's command.

        Keyword Args:
            tts_output (bool):      Is text-to-speech output enabled?
            userin:                 :class:`dragonfire.utilities.TextToAction` instance.
            user_prefix (str):      Prefix to address/call user when answering.
            is_server (bool):       Is Dragonfire running as an API server?

        Returns:
            str:  Response.

        .. note::

            Entry function for :class:`Omniscient` class. Dragonfire calls only this function. Unlike :func:`Learner.respond`, it executes TTS because of its late reponse nature.

        """

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
                        mention[ent.text] = 0.0  # the value if focus not even defined or the focus is NOT even mentioned
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
                                            mention[ent.text] += 1.0 * sentence.text.count(focus)  # assign the how many times the entity mentioned in the sentence

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

    def wordnet_entity_determiner(self, subject, tts_output, is_server, userin=None, user_prefix=None):
        """Function to determine the named entity classification of the subject.

        Args:
            subject (str):  Subject that extracted from the user's input/command.
            tts_output (bool):      Is text-to-speech output enabled?
            is_server (bool):   Is Dragonfire running as an API server?

        Keyword Args:
            userin:                 :class:`dragonfire.utilities.TextToAction` instance.
            user_prefix (str):      Prefix to address/call user when answering.

        Returns:
            (list) of (str)s: Entity list.

        .. note::

            `entity_samples_map` variable is used to fix some missing(or wrong) classififaction issue of spaCy NLP library detected while writing this code.

        """

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
            'QUANTITY': ['measurement', 'amount', 'distance', 'height', 'population'],
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

    def randomize_coefficients(self):
        """Function to randomize the coefficients for the purpose of optimizing their values.

        Returns:
            dict:  Randomized coefficients.

        .. note::

            This function is being used only for TESTING purposes.

        """
        coeff1 = round(uniform(0.00, 0.98), 2)
        coeff2 = round(uniform(0.00, (1 - coeff1)), 2)
        coeff3 = round(uniform(0.00, (1 - (coeff1 + coeff2))), 2)
        coeff4 = 1 - (coeff1 + coeff2 + coeff3)
        self.coefficient = {'frequency': coeff1, 'precedence': coeff2, 'proximity': coeff3, 'mention': coeff4}

    def phrase_cleaner(self, phrase):
        """Function to clean unnecessary words from the given phrase/string. (Punctuation mark, symbol, unknown, conjunction, determiner, subordinating or preposition and space)

        Args:
            phrase (str):  Noun phrase.

        Returns:
            str:  Cleaned noun phrase.
        """

        clean_phrase = []
        for word in self.nlp(phrase):
            if word.pos_ not in ['PUNCT', 'SYM', 'X', 'CONJ', 'DET', 'ADP', 'SPACE']:
                clean_phrase.append(word.text)
        return ' '.join(clean_phrase)

    def semantic_extractor(self, string):
        """Function to extract subject, subjects, focus, subject_with_objects from given string.

        Args:
            string (str):  String.

        Returns:
            (list) of (str)s: List of subject, subjects, focus, subject_with_objects.
        """

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
