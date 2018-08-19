# -*- coding: utf-8 -*-

"""
.. module:: test_api
    :platform: Unix
    :synopsis: tests for the api submodule.

.. moduleauthor:: Mehmet Mert Yıldıran <mert.yildiran@bil.omu.edu.tr>
"""

import json
import time
import os

import dragonfire
import dragonfire.api as API
from dragonfire.database import Base
from dragonfire.config import Config

import requests
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
import pytest


REG_KEY = "REG_KEY"
PORT = 3301
API_SERVER = 'http://localhost:' + str(PORT)
is_travis = 'TRAVIS' in os.environ

if is_travis:
    engine = create_engine('mysql+pymysql://' + Config.MYSQL_USER + ':' + Config.MYSQL_PASS + '@' + Config.MYSQL_HOST + '/' + Config.MYSQL_DB)
else:
    engine = create_engine('sqlite:///dragonfire.db', connect_args={'check_same_thread': False}, echo=True)
Base.metadata.create_all(engine)
Base.metadata.bind = engine
DBSession = sessionmaker(bind=engine)
db_session = DBSession()
dragonfire.learner.db_session = db_session
dragonfire.learner.is_server = True

api_ref = API.Run(dragonfire.nlp, dragonfire.learner, dragonfire.omniscient, dragonfire.dc, dragonfire.coref, dragonfire.userin, REG_KEY, PORT, db_session, dont_block=True)
time.sleep(5)


@pytest.fixture
def token():
    headers = {'Content-Type': 'application/x-www-form-urlencoded'}
    url = API_SERVER + '/register'
    params = {'name': 'John', 'gender': 'M', 'birth_date': '1990-01-01', 'reg_key': REG_KEY}
    response = requests.post(url, params=params, headers=headers)
    return json.loads(response.text)['token']


def test_api_tagger_end(token):
    headers = {'Content-Type': 'application/x-www-form-urlencoded', 'Authorization': token}
    url = API_SERVER + '/tag'
    params = {"text": "He is intelligent"}
    response = requests.post(url, params=params, headers=headers)
    assert json.loads(response.text) == [{'text': 'He', 'tag': 'PRP', 'is_stop': False, 'lemma': '-PRON-', 'dep': 'nsubj', 'pos': 'PRON', 'shape': 'Xx', 'is_alpha': True}, {'text': 'is', 'tag': 'VBZ', 'is_stop': True, 'lemma': 'be', 'dep': 'ROOT', 'pos': 'VERB', 'shape': 'xx', 'is_alpha': True}, {'text': 'intelligent', 'tag': 'JJ', 'is_stop': False, 'lemma': 'intelligent', 'dep': 'acomp', 'pos': 'ADJ', 'shape': 'xxxx', 'is_alpha': True}]


def test_api_dependency_parser_end(token):
    headers = {'Content-Type': 'application/x-www-form-urlencoded', 'Authorization': token}
    url = API_SERVER + '/dep'
    params = {"text": "He is intelligent"}
    response = requests.post(url, params=params, headers=headers)
    assert json.loads(response.text) == [{'root_head_text': 'is', 'text': 'He', 'root_text': 'He', 'root_dep': 'nsubj'}]


def test_api_entity_recognizer_end(token):
    headers = {'Content-Type': 'application/x-www-form-urlencoded', 'Authorization': token}
    url = API_SERVER + '/ner'
    params = {"text": "Albert Einstein was a German-born theoretical physicist who developed the theory of relativity"}
    response = requests.post(url, params=params, headers=headers)
    assert json.loads(response.text) == [{'start_char': 0, 'text': 'Albert Einstein', 'label': 'PERSON', 'end_char': 15}, {'start_char': 22, 'text': 'German', 'label': 'NORP', 'end_char': 28}]


def test_api_tokenizer_end(token):
    headers = {'Content-Type': 'application/x-www-form-urlencoded', 'Authorization': token}
    url = API_SERVER + '/token'
    params = {"text": "Albert Einstein was a German-born theoretical physicist who developed the theory of relativity"}
    response = requests.post(url, params=params, headers=headers)
    assert json.loads(response.text) == ['Albert', 'Einstein', 'was', 'a', 'German', '-', 'born', 'theoretical', 'physicist', 'who', 'developed', 'the', 'theory', 'of', 'relativity']


def test_api_sentence_segmenter_end(token):
    headers = {'Content-Type': 'application/x-www-form-urlencoded', 'Authorization': token}
    url = API_SERVER + '/sent'
    params = {"text": "Albert Einstein was a German-born theoretical physicist who developed the theory of relativity, one of the two pillars of modern physics. His work is also known for its influence on the philosophy of science."}
    response = requests.post(url, params=params, headers=headers)
    assert json.loads(response.text) == ['Albert Einstein was a German-born theoretical physicist who developed the theory of relativity, one of the two pillars of modern physics.', 'His work is also known for its influence on the philosophy of science.']


def test_api_cmd(token):
    headers = {'Content-Type': 'application/x-www-form-urlencoded', 'Authorization': token}
    url = API_SERVER + '/cmd'
    params = {"text": "He is intelligent"}
    response = requests.post(url, params=params, headers=headers)
    assert json.loads(response.text) == [{'tags': [{'text': 'He', 'tag': 'PRP', 'is_stop': False, 'lemma': '-PRON-', 'dep': 'nsubj', 'pos': 'PRON', 'shape': 'Xx', 'is_alpha': True}, {'text': 'is', 'tag': 'VBZ', 'is_stop': True, 'lemma': 'be', 'dep': 'ROOT', 'pos': 'VERB', 'shape': 'xx', 'is_alpha': True}, {'text': 'intelligent', 'tag': 'JJ', 'is_stop': False, 'lemma': 'intelligent', 'dep': 'acomp', 'pos': 'ADJ', 'shape': 'xxxx', 'is_alpha': True}], 'deps': [{'root_head_text': 'is', 'text': 'He', 'root_text': 'He', 'root_dep': 'nsubj'}], 'ners': []}]


def test_api_math(token):
    headers = {'Content-Type': 'application/x-www-form-urlencoded', 'Authorization': token}
    url = API_SERVER + '/math'
    params = {"text": "How much is 12 + 14?"}
    response = requests.post(url, params=params, headers=headers)
    assert json.loads(response.text) == '12 + 14 = 26'


def test_api_learn(token):
    headers = {'Content-Type': 'application/x-www-form-urlencoded', 'Authorization': token}
    url = API_SERVER + '/learn'
    params = {"text": "the Sun is hot", "user_id": 1}
    response = requests.post(url, params=params, headers=headers)
    assert json.loads(response.text) == 'OK, I get it. the Sun is hot'


def test_api_omni(token):
    headers = {'Content-Type': 'application/x-www-form-urlencoded', 'Authorization': token}
    url = API_SERVER + '/omni'
    params = {"text": "Where is the Times Square?", "gender_prefix": "sir"}
    response = requests.post(url, params=params, headers=headers)
    assert json.loads(response.text) == 'New York City'


def test_api_deep(token):
    headers = {'Content-Type': 'application/x-www-form-urlencoded', 'Authorization': token}
    url = API_SERVER + '/deep'
    params = {"text": "Do you like to listen music?", "gender_prefix": "sir"}
    response = requests.post(url, params=params, headers=headers)
    assert json.loads(response.text) == 'Of course.'


def test_api_wikipedia(token):
    headers = {'Content-Type': 'application/x-www-form-urlencoded', 'Authorization': token}
    url = API_SERVER + '/wikipedia'
    params = {"query": "Albert Einstein", "gender_prefix": "sir"}
    response = requests.post(url, params=params, headers=headers)
    assert json.loads(response.text) == {'url': 'https://en.wikipedia.org/wiki/Albert_Einstein', 'response': 'Albert Einstein ; 14 March 1879   18 April 1955) was a German-born theoretical physicist who developed the theory of relativity, one of the two pillars of modern physics . His work is also known for its influence on the philosophy of science. He is best known to the general public for his mass energy equivalence formula E = mc2, which has been dubbed "the world\'s most famous equation".'}


def test_api_youtube(token):
    headers = {'Content-Type': 'application/x-www-form-urlencoded', 'Authorization': token}
    url = API_SERVER + '/youtube'
    params = {"query": "Turn Down for What", "gender_prefix": "sir"}
    response = requests.post(url, params=params, headers=headers)
    assert json.loads(response.text) == {'url': 'https://www.youtube.com/watch?v=HMUDVMiITOU', 'response': 'DJ Snake, Lil Jon - Turn Down for What'}
