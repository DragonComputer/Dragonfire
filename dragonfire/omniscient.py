from dragonfire.utilities import Data
import wikipedia
import spacy
import collections
from nltk.corpus import wordnet as wn
import random

class Engine():

    def __init__(self):
        self.nlp = spacy.load('en')
        self.entity_map = {
                'WHO': ['PERSON'],
                'WHAT': ['PERSON','NORP','FACILITY','ORG','GPE','LOC','PRODUCT','EVENT','WORK_OF_ART','LANGUAGE','DATE','TIME','PERCENT','MONEY','QUANTITY','ORDINAL','CARDINAL'],
                'WHEN': ['DATE','TIME','EVENT'],
                'WHERE': ['FACILITY','GPE','LOC']
        }
        self.coefficient = {'frequency': 0.27, 'precedence': 0.27, 'proximity': 0.23, 'mention': 0.23}

    def respond(self,com,tts_output=False):
        userin = Data([" "]," ")
        doc = self.nlp(com.decode('utf-8'))
        query = None
        subjects = []
        pobjects = []
        dobjects = []
        for np in doc.noun_chunks:
            #print(np.text, np.root.text, np.root.dep_, np.root.head.text)
            if (np.root.dep_ == 'nsubj' or np.root.dep_ == 'nsubjpass') and np.root.tag_ != 'WP':
                subjects.append(np.text.encode('utf-8'))
            if np.root.dep_ == 'pobj':
                pobjects.append(np.text.encode('utf-8'))
            if np.root.dep_ == 'dobj':
                dobjects.append(np.text.encode('utf-8'))
        if pobjects:
            query = ' '.join(pobjects)
        elif subjects:
            query = ' '.join(subjects)
        elif dobjects:
            query = ' '.join(dobjects)
        else:
            if not tts_output: print "Sorry, I don't understand the subject of your question."
            if tts_output: userin.say("Sorry, I don't understand the subject of your question.")
            return False

        focus = None
        if dobjects:
            focus = self.phrase_cleaner(' '.join(dobjects))
        elif subjects:
            focus = self.phrase_cleaner(' '.join(subjects))
        elif pobjects:
            focus = self.phrase_cleaner(' '.join(pobjects))
        if focus in query: focus = None

        subject_with_objects = []
        for dobject in dobjects:
            subject_with_objects.append(dobject)
        for subject in subjects:
            subject_with_objects.append(subject)
        for pobject in pobjects:
            subject_with_objects.append(pobject)
        subject_with_objects = ' '.join(subject_with_objects)

        if query:
            if tts_output: userin.say("Please wait...", True, False)
            wh_question = []
            for word in doc:
				if word.tag_ in ['WDT','WP','WP$','WRB']:
					wh_question.append(word.text.upper())
            findings = []
            nth_page = 0
            while not findings:
                page = wikipedia.page(wikipedia.search(query)[nth_page])
                nth_page += 1
                if nth_page > 5: break
                wiki_doc = self.nlp(page.content)
                sentences = [sent.string.strip() for sent in wiki_doc.sents]
                #return [' '.join(subjects),' '.join(pobjects)]
                all_entities = []
                mention = {}
                subject_entities_by_wordnet = None
                if 'WHAT' in wh_question:
                    subject_entities_by_wordnet = self.wordnet_entity_determiner(subject_with_objects,tts_output)
                for sentence in reversed(sentences):
                    sentence = self.nlp(sentence)
                    for ent in sentence.ents:
                        all_entities.append(ent.text)
                        for wh in wh_question:
                            if self.entity_map.has_key(wh.upper()):
                                target_entities = self.entity_map[wh.upper()]
                                if wh.upper() == 'WHAT':
                                    target_entities = []
                                    for subject_entity_by_wordnet in subject_entities_by_wordnet:
                                        target_entities.append(subject_entity_by_wordnet)
                                if ent.label_ in target_entities:
                                    findings.append(ent.text)
                                    if focus:
                                        if focus in sentence.text:
                                            mention[ent.text] = 1.0 #* sentence.text.count(focus)
                                        else:
                                            mention[ent.text] = 0.0
                                    else:
                                        mention[ent.text] = 0.0

            if findings:
                frequency = collections.Counter(findings)
                max_freq = max(frequency.values())
                for key, value in frequency.iteritems():
                    frequency[key] = float(value) / max_freq

                precedence = {}
                unique = list(set(findings))
                for i in range(len(unique)):
                    precedence[unique[i]] = float(len(unique) - i) / len(unique)

                proximity = {}
                subject_indices = []
                for i in range(len(all_entities)):
                    for subject in subjects:
                        for word in subject.split():
                            if word in all_entities[i]:
                                subject_indices.append(i)
                for i in range(len(all_entities)):
                    for index in subject_indices:
                        inverse_distance = float((len(all_entities) - 1) - abs(i - index)) / (len(all_entities) - 1)
                        if proximity.has_key(all_entities[i]):
                            proximity[all_entities[i]] = (proximity[all_entities[i]] + inverse_distance) / 2
                        else:
                            proximity[all_entities[i]] = inverse_distance
                    if not proximity.has_key(all_entities[i]):
                            proximity[all_entities[i]] = 0

                ranked = {}
                for key, value in frequency.iteritems():
                    if key not in query:
                        ranked[key] = value * self.coefficient['frequency'] + precedence[key] * self.coefficient['precedence'] + proximity[key] * self.coefficient['proximity'] + mention[key] * self.coefficient['mention']
                if not tts_output: print sorted(ranked.items(), key=lambda x:x[1])[::-1][:5]
                if tts_output: userin.say(sorted(ranked.items(), key=lambda x:x[1])[::-1][0][0], True, True)
                return sorted(ranked.items(), key=lambda x:x[1])[::-1][0][0]
            else:
                if not tts_output: print "Sorry, I couldn't find anything worthy to answer your question."
                if tts_output: userin.say("Sorry, I couldn't find anything worthy to answer your question.", True, True)
                return False

    def wordnet_entity_determiner(self,subject,tts_output):
        print subject
        entity_samples_map = {
                'PERSON': ['person','character','human','individual','name'],
                'NORP': ['nationality','religion','politics'],
                'FACILITY': ['building','airport','highway','bridge','port'],
                'ORG': ['company','agency','institution','university'],
                'GPE': ['country','city','state','address','capital'],
                'LOC': ['geography','mountain','ocean','river'],
                'PRODUCT': ['product','object','vehicle','food'],
                'EVENT': ['hurricane','battle','war','sport'],
                'WORK_OF_ART': ['art','book','song','painting'],
                'LANGUAGE': ['language','accent','dialect','speech'],
                'DATE': ['year','month','day'],
                'TIME': ['time','hour','minute'],
                'PERCENT': ['percent','rate','ratio','fee'],
                'MONEY': ['money','cash','salary','wealth'],
                'QUANTITY': ['measurement','amount','distance','height','population'],
                'ORDINAL': ['ordinal','first','second','third'],
                'CARDINAL': ['cardinal','number','amount','mathematics']
        }
        doc = self.nlp(subject.decode('utf-8'))
        subject = []
        for word in doc:
            #if word.pos_ not in ['PUNCT','SYM','X','CONJ','DET','ADP','SPACE']:
            if word.pos_ == 'NOUN':
                subject.append(word.text.lower())
        entity_scores = {}
        for entity, samples in entity_samples_map.iteritems():
            entity_scores[entity] = 0
            for sample in samples:
                sample_wn = wn.synset(sample + '.n.01')
                for word in subject:
                    word_wn = wn.synset(word + '.n.01')
                    entity_scores[entity] += word_wn.path_similarity(sample_wn)
            entity_scores[entity] = entity_scores[entity] / len(samples)
        if not tts_output: print sorted(entity_scores.items(), key=lambda x:x[1])[::-1][:3]
        result = sorted(entity_scores.items(), key=lambda x:x[1])[::-1][0][0]
        if result == 'FACILITY': return [result,'ORG']
        if result == 'PRODUCT': return [result,'ORG']
        return [result]

    def randomize_coefficients(self):
        coeff1 = round(random.uniform(0.00, 0.98),2)
        coeff2 = round(random.uniform(0.00, (1 - coeff1)),2)
        coeff3 = round(random.uniform(0.00, (1 - (coeff1 + coeff2))),2)
        coeff4 = 1 - (coeff1 + coeff2 + coeff3)
        self.coefficient = {'frequency': coeff1, 'precedence': coeff2, 'proximity': coeff3, 'mention': coeff4}

    def phrase_cleaner(self,phrase):
        clean_phrase = []
        for word in self.nlp(phrase.decode('utf-8')):
            if word.pos_ not in ['PUNCT','SYM','X','CONJ','DET','ADP','SPACE']:
                clean_phrase.append(word.text)
        return ' '.join(clean_phrase)


if __name__ == "__main__":

    EngineObj = Engine()
    best_score = 0
    best_coefficient = None
    for i in range(1):
        print "Counter: " + str(i)
        score = 0
        #EngineObj.randomize_coefficients()
        print EngineObj.coefficient

        # New York City
        print "\nWhere is the Times Square"
        if EngineObj.respond("Where is the Times Square") == "New York City": score += 1

        # 2,720 ft - QUANTITY
        print "\nWhat is the height of Burj Khalifa"
        if EngineObj.respond("What is the height of Burj Khalifa") == "2,720 ft": score += 1

        # Dubai
        print "\nWhere is Burj Khalifa"
        if EngineObj.respond("Where is Burj Khalifa") == "Dubai": score += 1

        # 481 feet - QUANTITY
        print "\nWhat is the height of Great Pyramid of Giza"
        if EngineObj.respond("What is the height of Great Pyramid of Giza") == "(481 feet": score += 1

        # Kit Harington
        print "\nWho is playing Jon Snow in Game of Thrones"
        if EngineObj.respond("Who is playing Jon Snow in Game of Thrones") == "Kit Harington": score += 1

        # 8 - CARDINAL
        print "\nWhat is the atomic number of oxygen"
        if EngineObj.respond("What is the atomic number of oxygen") == "8": score += 1

        # 1.371 billion - QUANTITY
        print "\nWhat is the population of China"
        if EngineObj.respond("What is the population of China") == "1.371 billion": score += 1

        # Japanese - LANGUAGE
        print "\nWhat is the official language of Japan"
        if EngineObj.respond("What is the official language of Japan") == "Japanese": score += 1

        # Stark - PERSON
        print "\nWhat is the real name of Iron Man"
        if EngineObj.respond("What is the real name of Iron Man") == "Stark": score += 1

        # Mehmed The Conqueror
        print "\nWho is the conqueror of Constantinople"
        if EngineObj.respond("Who is the conqueror of Constantinople") == "Mehmed The Conqueror": score += 1

        # 1453
        print "\nWhen Constantinople was conquered"
        if EngineObj.respond("When Constantinople was conquered") == "1453": score += 1

        # Ankara - GPE
        print "\nWhat is the capital of Turkey"
        if EngineObj.respond("What is the capital of Turkey") == "Ankara": score += 1

        # Istanbul - GPE
        print "\nWhat is the largest city of Turkey"
        if EngineObj.respond("What is the largest city of Turkey") == "Istanbul": score += 1

        # Hinduism - NORP
        print "\nWhat is the oldest religion"
        if EngineObj.respond("What is the oldest religion") == "Hinduism": score += 1

        # Hartsfield Jackson Atlanta International Airport - FACILITY
        print "\nWhat is the world's busiest airport"
        if EngineObj.respond("What is the world's busiest airport") == "Hartsfield Jackson Atlanta International Airport": score += 1

        # Princeton University - ORG
        print "\nWhat is the name of the world's best university"
        if EngineObj.respond("What is the name of the world's best university") == "Princeton University": score += 1

        # Nile river - LOC
        print "\nWhat is the name of the world's longest river"
        if EngineObj.respond("What is the name of the world's longest river") == "Nile river": score += 1

        # Rolls-Royce - PRODUCT
        print "\nWhat is the brand of the world's most expensive car"
        if EngineObj.respond("What is the brand of the world's most expensive car") == "Rolls-Royce": score += 1

        # World War II - EVENT
        print "\nWhat is the bloodiest war in human history"
        if EngineObj.respond("What is the bloodiest war in human history") == "World War II": score += 1

        # Da Vinci Code - WORK_OF_ART
        print "\nWhat is the name of the best seller book"
        if EngineObj.respond("What is the name of the best seller book") == "Da Vinci Code": score += 1

        if score > best_score:
            print "\n--- !!! NEW BEST !!! ---"
            best_score = score
            best_coefficient = EngineObj.coefficient
            print str(best_score) + ' / 20'
            print best_coefficient
            print "--- !!! NEW BEST !!! ---\n"
