from __future__ import print_function
import hug
from hug_middleware_cors import CORSMiddleware
import waitress
from threading import Thread
import json
from dragonfire.omniscient import Engine
from dragonfire.conversational import DeepConversation
from dragonfire.learn import Learner
from dragonfire.config import Config
from dragonfire.arithmetic import arithmetic_parse
import wikipedia as wikipedia_lib
import re
import youtube_dl
import pymysql
import random

nlp = None
omniscient = None
userin = None
dc = None
learner = None
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


@hug.post('/wikipedia', requires=token_authentication)
def wikipedia(query, gender_prefix):
    response = ""
    url = ""
    wikiresult = wikipedia_lib.search(query)
    if len(wikiresult) == 0:
        response = "Sorry, " + gender_prefix + ". But I couldn't find anything about " + query + " in Wikipedia."
    else:
        wikipage = wikipedia_lib.page(wikiresult[0])
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


@hug.post('/youtube', requires=token_authentication)
def youtube(query, gender_prefix):
    response = ""
    url = ""
    info = youtube_dl.YoutubeDL({}).extract_info('ytsearch:' + query, download=False, ie_key='YoutubeSearch')
    if len(info['entries']) > 0:
        response = info['entries'][0]['title']
        url = "https://www.youtube.com/watch?v=%s" % (info['entries'][0]['id'])
        response = "".join([
            i if ord(i) < 128 else ' '
            for i in response
        ])
    else:
        response = "No video found, " + gender_prefix + "."
    data = {}
    data['response'] = response
    data['url'] = url
    return json.dumps(data, indent=4)


@hug.post('/learn', requires=token_authentication)
def learn(text, user_id):
    response = learner.respond(text, is_server=True, user_id=user_id)
    if not response:
        response = ""
    return json.dumps(response, indent=4)


@hug.post('/math', requires=token_authentication)
def math(text):
    response = arithmetic_parse(text)
    if not response:
        response = ""
    return json.dumps(response, indent=4)


@hug.post('/notification', requires=token_authentication)
def notification(user_id, location, gender_prefix):
    url = ""
    title = ""
    message = ""

    db = pymysql.connect(Config.MYSQL_HOST, Config.MYSQL_USER, Config.MYSQL_PASS, Config.MYSQL_DB)
    cursor = db.cursor(pymysql.cursors.DictCursor)
    sql1 = "SELECT * FROM users WHERE id = {}".format(user_id)
    sql2 = "SELECT * FROM notifications"
    try:
        cursor.execute(sql1)
        results = cursor.fetchall()
        if results:
            row = results[0]
            name = row["name"]
            gender = row["gender"]
            birth_date = row["birth_date"]
        else:
            name = "Master"
            gender = 1
            birth_date = "1980-01-01"

        cursor.execute(sql2)
        results = cursor.fetchall()
        row = random.choice(results)
        if row["capitalize"] == 1:
            gender_prefix = gender_prefix.capitalize()
        url = row["url"]
        title = row["title"]
        message = row["message"].format(gender_prefix, name)
    except pymysql.InternalError as error:
        code, message = error.args
        print (">>>>>>>>>>>>>", code, message)
    db.close()

    data = {}
    data['url'] = url
    data['title'] = title
    data['message'] = message
    return json.dumps(data, indent=4)


@hug.post('/register', requires=token_authentication)
def register(name, gender, birth_date):
    id = ""

    db = pymysql.connect(Config.MYSQL_HOST, Config.MYSQL_USER, Config.MYSQL_PASS, Config.MYSQL_DB)
    cursor = db.cursor(pymysql.cursors.DictCursor)
    sql = """
        INSERT INTO users (name, gender, birth_date)
        VALUES('{}', '{}', '{}')
        """.format(name, gender, birth_date)
    try:
        cursor.execute(sql)
        db.commit()
        id = cursor.lastrowid
    except pymysql.InternalError as error:
        code, message = error.args
        print (">>>>>>>>>>>>>", code, message)
    db.close()

    return json.dumps(id, indent=4)


class Run():
    def __init__(self, nlp_ref, userin_ref, token, port_number):
        global nlp
        global omniscient
        global userin
        global dc
        global precomptoken
        global learner
        nlp = nlp_ref  # Load en_core_web_sm, English, 50 MB, default model
        omniscient = Engine(nlp)
        dc = DeepConversation()
        learner = Learner(nlp)
        userin = userin_ref
        precomptoken = token
        app = hug.API(__name__)
        app.http.output_format = hug.output_format.text
        app.http.add_middleware(CORSMiddleware(app))
        t = Thread(target=waitress.serve, args=(__hug_wsgi__, ), kwargs={"port": port_number})
        t.start()
        t.join()


if __name__ == '__main__':
    app = hug.API(__name__)
    app.http.output_format = hug.output_format.text
    app.http.add_middleware(CORSMiddleware(app))
    waitress.serve(__hug_wsgi__, port=8000)
