import wikipedia
import spacy
import collections

class Engine():

    def __init__(self):
        self.nlp = spacy.load('en')
        self.entity_map = {
                'WHO': ['PERSON'],
                'WHAT': ['NORP','FACILITY','ORG','GPE','LOC','PRODUCT','EVENT','WORK_OF_ART','LANGUAGE','DATE','TIME','PERCENT','MONEY','QUANTITY','ORDINAL','CARDINAL'],
                'WHEN': ['DATE','TIME','EVENT'],
                'WHERE': ['FACILITY','GPE','LOC']
        }
        self.coefficient = {'frequency': 0.3, 'precedence': 0.1, 'proximity': 0.5}

    def respond(self,com):
        doc = self.nlp(com.decode('utf-8'))
        query = None
        result = []
        subjects = []
        objects = []
        for np in doc.noun_chunks:
            #print(np.text, np.root.text, np.root.dep_, np.root.head.text)
            #result.append((np.text,np.root.dep_))
            if np.root.dep_ == 'nsubj' and np.root.tag_ != 'WP':
                subjects.append(np.text.encode('utf-8'))
            if np.root.dep_ == 'pobj':
                objects.append(np.text.encode('utf-8'))
        if objects:
            query = ' '.join(objects)
        elif subjects:
            query = ' '.join(subjects)
        else:
            return "SORRY, I DON'T UNDERSTAND YOUR QUESTION"

        if query:
            wh_question = []
            for word in doc:
				if word.tag_ in ['WDT','WP','WP$','WRB']:
					wh_question.append(word.text)
            page = wikipedia.page(wikipedia.search(query)[0])
            wiki_doc = self.nlp(page.content)
            sentences = [sent.string.strip() for sent in wiki_doc.sents]
            #return [' '.join(subjects),' '.join(objects)]
            all_entities = []
            findings = []
            for sentence in reversed(sentences):
                sentence = self.nlp(sentence)
                for ent in sentence.ents:
                    all_entities.append(ent.text)
                    for wh in wh_question:
                        if self.entity_map.has_key(wh.upper()):
                            if ent.label_ in self.entity_map[wh.upper()]:
                                findings.append(ent.text)

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
            for i in range(len(findings)):
                for subject in subjects:
                    for word in subject.split():
                        if word in findings[i]:
                            subject_indices.append(i)
            for i in range(len(findings)):
                for index in subject_indices:
                    inverse_distance = float((len(findings) - 1) - abs(i - index)) / (len(findings) - 1)
                    if proximity.has_key(findings[i]):
                        proximity[findings[i]] = (proximity[findings[i]] + inverse_distance) / 2
                    else:
                        proximity[findings[i]] = inverse_distance
                if not proximity.has_key(findings[i]):
                        proximity[findings[i]] = 0

            ranked = {}
            for key, value in frequency.iteritems():
                if key not in query:
                    ranked[key.upper()] = value * self.coefficient['frequency'] + precedence[key] * self.coefficient['precedence'] + proximity[key] * self.coefficient['proximity']
            return sorted(ranked.items(), key=lambda x:x[1])[::-1][:5]

if __name__ == "__main__":
    EngineObj = Engine()
    print "Where is the Times Square"
    print EngineObj.respond("Where is the Times Square")

    print "What is the height of Burj Khalifa"
    print EngineObj.respond("What is the height of Burj Khalifa")

    print "Where is Burj Khalifa"
    print EngineObj.respond("Where is Burj Khalifa")

    print "What is the height of Great Pyramid of Giza"
    print EngineObj.respond("What is the height of Great Pyramid of Giza")

    print "Who is playing Jon Snow in Game of Thrones"
    print EngineObj.respond("Who is playing Jon Snow in Game of Thrones")

    print "What is the atomic number of oxygen"
    print EngineObj.respond("What is the atomic number of oxygen")

    print "What is the population of China"
    print EngineObj.respond("What is the population of China")

    print "What is the real name of Iron Man"
    print EngineObj.respond("What is the real name of Iron Man")

    print "Who is the conqueror of Constantinople"
    print EngineObj.respond("Who is the conqueror of Constantinople")

    print "When Constantinople was conquered"
    print EngineObj.respond("When Constantinople was conquered")

    print "What is the capital of Turkey"
    print EngineObj.respond("What is the capital of Turkey")

    print "What is the largest city of Turkey"
    print EngineObj.respond("What is the largest city of Turkey")
