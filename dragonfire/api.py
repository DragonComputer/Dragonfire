from __future__ import print_function
import collections  # Imported to support ordered dictionaries in Python
import hug
from hug_middleware_cors import CORSMiddleware
import waitress
from threading import Thread
import json

nlp = None

@hug.get('/tag')
def tagger(text):
    data = collections.OrderedDict()
    doc = nlp(text)
    for token in doc:
        parse = {
            'lemma': token.lemma_,
            'pos': token.pos_,
            'tag': token.tag_,
            'dep': token.dep_,
            'shape': token.shape_,
            'is_alpha': token.is_alpha,
            'is_stop': token.is_stop
            }
        data[token.text] = parse
    return json.dumps(data, indent=4)

@hug.get('/dep')
def dependency_parser(text):
    data = collections.OrderedDict()
    doc = nlp(text)
    for chunk in doc.noun_chunks:
        parse = {
            'root_text': chunk.root.text,
            'root_dep': chunk.root.dep_,
            'root_head_text': chunk.root.head.text,
            }
        data[chunk.text] = parse
    return json.dumps(data, indent=4)

@hug.get('/ner')
def entity_recognizer(text):
    data = collections.OrderedDict()
    doc = nlp(text)
    for ent in doc.ents:
        parse = {
            'start_char': ent.start_char,
            'end_char': ent.end_char,
            'label': ent.label_,
            }
        data[ent.text] = parse
    return json.dumps(data, indent=4)

@hug.get('/token')
def tokenizer(text):
    data = []
    doc = nlp(text)
    for token in doc:
        data.append(token.text)
    return json.dumps(data, indent=4)

@hug.get('/sent')
def sentence_segmenter(text):
    data = []
    doc = nlp(text)
    for sent in doc.sents:
        data.append(sent.text)
    return json.dumps(data, indent=4)


class Run():
    def __init__(self, nlpRef):
        global nlp
        nlp = nlpRef  # Load en_core_web_sm, English, 50 MB, default model
        app = hug.API(__name__)
        app.http.output_format = hug.output_format.text
        app.http.add_middleware(CORSMiddleware(app))
        t = Thread(target=waitress.serve, args=(__hug_wsgi__, ), kwargs={"port": 3301})
        t.start()
        t.join()


if __name__ == '__main__':
    app = hug.API(__name__)
    app.http.output_format = hug.output_format.text
    app.http.add_middleware(CORSMiddleware(app))
    waitress.serve(__hug_wsgi__, port=8000)
