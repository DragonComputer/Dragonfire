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
        self.coefficient = {'frequency': 0.3, 'precedence': 0.2, 'proximity': 0.5}

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
            findings = []
            for sentence in reversed(sentences):
                sentence = self.nlp(sentence)
                for ent in sentence.ents:
                    for wh in wh_question:
                        if self.entity_map.has_key(wh):
                            if ent.label_ in self.entity_map[wh]:
                                findings.append(ent.text.upper())

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
                if findings[i] in subjects:
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
                ranked[key] = value * self.coefficient['frequency'] + precedence[key] * self.coefficient['precedence'] + proximity[key] * self.coefficient['proximity']
            return sorted(ranked.items(), key=lambda x:x[1])[::-1][:5]

if __name__ == "__main__":
    EngineObj = Engine()
    print "WHERE IS THE TIMES SQUARE"
    print EngineObj.respond("WHERE IS THE TIMES SQUARE")

    print "WHAT IS THE HEIGHT OF BURJ KHALIFA"
    print EngineObj.respond("WHAT IS THE HEIGHT OF BURJ KHALIFA")

    print "WHERE IS BURJ KHALIFA"
    print EngineObj.respond("WHERE IS BURJ KHALIFA")

    print "WHAT IS THE HEIGHT OF GREAT PYRAMID OF GIZA"
    print EngineObj.respond("WHAT IS THE HEIGHT OF GREAT PYRAMID OF GIZA")

    print "WHO IS PLAYING JON SNOW IN GAME OF THRONES"
    print EngineObj.respond("WHO IS PLAYING JON SNOW IN GAME OF THRONES")

    print "WHAT IS THE ATOMIC NUMBER OF OXYGEN"
    print EngineObj.respond("WHAT IS THE ATOMIC NUMBER OF OXYGEN")

    print "WHAT IS THE POPULATION OF CHINA"
    print EngineObj.respond("WHAT IS THE POPULATION OF CHINA")

    print "WHAT IS THE REAL NAME OF IRON MAN"
    print EngineObj.respond("WHAT IS THE REAL NAME OF IRON MAN")

    print "WHO IS THE CONQUEROR OF CONSTANTINOPLE"
    print EngineObj.respond("WHO IS THE CONQUEROR OF CONSTANTINOPLE")

    print "WHEN CONSTANTINOPLE WAS CONQUERED"
    print EngineObj.respond("WHEN CONSTANTINOPLE WAS CONQUERED")

    print "WHAT IS THE CAPITAL OF TURKEY"
    print EngineObj.respond("WHAT IS THE CAPITAL OF TURKEY")

    print "WHAT IS THE LARGEST CITY OF TURKEY"
    print EngineObj.respond("WHAT IS THE LARGEST CITY OF TURKEY")
