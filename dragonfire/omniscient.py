import wikipedia
import spacy

class Engine():

    def __init__(self):
        self.nlp = spacy.load('en')

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
            page = wikipedia.page(wikipedia.search(query)[0])
            doc = self.nlp(page.content)
            sentences = [sent.string.strip() for sent in doc.sents]
            return sentences[0]

if __name__ == "__main__":
    EngineObj = Engine()
    print EngineObj.respond("WHERE IS THE TIMES SQUARE")
    print EngineObj.respond("WHAT IS THE HEIGHT OF BURJ KHALIFA")
    print EngineObj.respond("WHERE IS BURJ KHALIFA")
    print EngineObj.respond("WHAT IS THE HEIGHT OF GREAT PYRAMID OF GIZA")
    print EngineObj.respond("WHO IS PLAYING JON SNOW IN GAME OF THRONES")
    print EngineObj.respond("WHAT IS THE ATOMIC NUMBER OF OXYGEN")
    print EngineObj.respond("WHAT IS THE POPULATION OF CHINA")
    print EngineObj.respond("WHAT IS THE REAL NAME OF IRON MAN")
    print EngineObj.respond("WHO IS THE CONQUEROR OF CONSTANTINOPLE")
    print EngineObj.respond("WHEN CONSTANTINOPLE WAS CONQUERED")
    print EngineObj.respond("WHAT IS THE CAPITAL OF TURKEY")
    print EngineObj.respond("WHAT IS THE LARGEST CITY OF TURKEY")
