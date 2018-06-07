from __future__ import print_function
import collections  # Imported to support ordered dictionaries in Python
import hug
from hug_middleware_cors import CORSMiddleware
import waitress
from threading import Thread
import json
from dragonfire.omniscient import Engine
from dragonfire.conversational import DeepConversation
import wikipedia
import re

nlp = None
omniscient = None
userin = None
dc = None
precomptoken = None

@hug.authentication.token
def token_authentication(token):
    if token == precomptoken:
        return True

@hug.post('/tag', requires=token_authentication)
def tagger_end(text):
    return json.dumps(tagger(text), indent=4)

def tagger(text):
    data = []
    doc = nlp(text)
    for token in doc:
        parse = {
            'text': token.text,
            'lemma': token.lemma_,
            'pos': token.pos_,
            'tag': token.tag_,
            'dep': token.dep_,
            'shape': token.shape_,
            'is_alpha': token.is_alpha,
            'is_stop': token.is_stop
            }
        data.append(parse)
    return data

@hug.post('/dep', requires=token_authentication)
def dependency_parser_end(text):
    return json.dumps(dependency_parser(text), indent=4)

def dependency_parser(text):
    data = []
    doc = nlp(text)
    for chunk in doc.noun_chunks:
        parse = {
            'text': chunk.text,
            'root_text': chunk.root.text,
            'root_dep': chunk.root.dep_,
            'root_head_text': chunk.root.head.text,
            }
        data.append(parse)
    return data

@hug.post('/ner', requires=token_authentication)
def entity_recognizer_end(text):
    return json.dumps(entity_recognizer(text), indent=4)

def entity_recognizer(text):
    data = []
    doc = nlp(text)
    for ent in doc.ents:
        parse = {
            'text': ent.text,
            'start_char': ent.start_char,
            'end_char': ent.end_char,
            'label': ent.label_,
            }
        data.append(parse)
    return data

@hug.post('/token', requires=token_authentication)
def tokenizer_end(text):
    return json.dumps(tokenizer(text), indent=4)

def tokenizer(text):
    data = []
    doc = nlp(text)
    for token in doc:
        data.append(token.text)
    return data

@hug.post('/sent', requires=token_authentication)
def sentence_segmenter_end(text):
    return json.dumps(sentence_segmenter(text), indent=4)

def sentence_segmenter(text):
    data = []
    doc = nlp(text)
    for sent in doc.sents:
        data.append(sent.text)
    return data

@hug.post('/cmd', requires=token_authentication)
def cmd(text):
    return json.dumps(all_in_one(text), indent=4)

def all_in_one(text):
    data = []
    sents = sentence_segmenter(text)
    for sent in sents:
        sent_data = {}
        sent_data['tags'] = tagger(sent)
        sent_data['deps'] = dependency_parser(sent)
        sent_data['ners'] = entity_recognizer(sent)
        data.append(sent_data)
    return data

@hug.post('/omni', requires=token_authentication)
def omni(text, gender_prefix):
    answer = omniscient.respond(text, userin=userin, user_prefix=gender_prefix, is_server=True)
    if not answer:
        answer = ""
    return json.dumps(answer, indent=4)

@hug.post('/deep', requires=token_authentication)
def deep(text, gender_prefix):
    answer = dc.respond(text, user_prefix=gender_prefix)
    return json.dumps(answer, indent=4)

@hug.post('/wiki', requires=token_authentication)
def wiki(query, gender_prefix):
    response = ""
    url = ""
    wikiresult = wikipedia.search(query)
    if len(wikiresult) == 0:
        response = "Sorry, " + gender_prefix + ". But I couldn't find anything about " + query + " in Wikipedia."
    else:
        wikipage = wikipedia.page(wikiresult[0])
        wikicontent = "".join([
            i if ord(i) < 128 else ' '
            for i in wikipage.content
        ])
        wikicontent = re.sub(r'\([^)]*\)', '', wikicontent)
        response = " ".join(sentence_segmenter(wikicontent)[:3])
        url = wikipage.url
    data = {}
    data['response'] = response
    data['url'] = url
    return json.dumps(data, indent=4)


class Run():
    def __init__(self, nlpRef, userinRef, token):
        global nlp
        global omniscient
        global userin
        global dc
        global precomptoken
        nlp = nlpRef  # Load en_core_web_sm, English, 50 MB, default model
        omniscient = Engine(nlp)
        dc = DeepConversation()
        userin = userinRef
        precomptoken = token
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
