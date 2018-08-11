# -*- coding: utf-8 -*-

"""
.. module:: test_api
    :platform: Unix
    :synopsis: tests for the api submodule.

.. moduleauthor:: Mehmet Mert Yıldıran <mert.yildiran@bil.omu.edu.tr>
"""

import json

import dragonfire
import dragonfire.api as API

import pytest


API.nlp = dragonfire.nlp
API.learner = dragonfire.learner
API.omniscient = dragonfire.omniscient
API.dc = dragonfire.dc
API.userin = dragonfire.userin


def test_api_tagger_end():
    assert json.loads(API.tagger_end("He is intelligent")) == [{'text': 'He', 'tag': 'PRP', 'is_stop': False, 'lemma': '-PRON-', 'dep': 'nsubj', 'pos': 'PRON', 'shape': 'Xx', 'is_alpha': True}, {'text': 'is', 'tag': 'VBZ', 'is_stop': True, 'lemma': 'be', 'dep': 'ROOT', 'pos': 'VERB', 'shape': 'xx', 'is_alpha': True}, {'text': 'intelligent', 'tag': 'JJ', 'is_stop': False, 'lemma': 'intelligent', 'dep': 'acomp', 'pos': 'ADJ', 'shape': 'xxxx', 'is_alpha': True}]


def test_api_dependency_parser_end():
    assert json.loads(API.dependency_parser_end("He is intelligent")) == [{'root_head_text': 'is', 'text': 'He', 'root_text': 'He', 'root_dep': 'nsubj'}]


def test_api_entity_recognizer_end():
    assert json.loads(API.entity_recognizer_end("Albert Einstein was a German-born theoretical physicist who developed the theory of relativity")) == [{'start_char': 0, 'text': 'Albert Einstein', 'label': 'PERSON', 'end_char': 15}, {'start_char': 22, 'text': 'German', 'label': 'NORP', 'end_char': 28}]


def test_api_tokenizer_end():
    assert json.loads(API.tokenizer_end("Albert Einstein was a German-born theoretical physicist who developed the theory of relativity")) == ['Albert', 'Einstein', 'was', 'a', 'German', '-', 'born', 'theoretical', 'physicist', 'who', 'developed', 'the', 'theory', 'of', 'relativity']


def test_api_sentence_segmenter_end():
    assert json.loads(API.sentence_segmenter_end("Albert Einstein was a German-born theoretical physicist who developed the theory of relativity, one of the two pillars of modern physics. His work is also known for its influence on the philosophy of science.")) == ['Albert Einstein was a German-born theoretical physicist who developed the theory of relativity, one of the two pillars of modern physics.', 'His work is also known for its influence on the philosophy of science.']


def test_api_cmd():
    assert json.loads(API.cmd("He is intelligent")) == [{'tags': [{'text': 'He', 'tag': 'PRP', 'is_stop': False, 'lemma': '-PRON-', 'dep': 'nsubj', 'pos': 'PRON', 'shape': 'Xx', 'is_alpha': True}, {'text': 'is', 'tag': 'VBZ', 'is_stop': True, 'lemma': 'be', 'dep': 'ROOT', 'pos': 'VERB', 'shape': 'xx', 'is_alpha': True}, {'text': 'intelligent', 'tag': 'JJ', 'is_stop': False, 'lemma': 'intelligent', 'dep': 'acomp', 'pos': 'ADJ', 'shape': 'xxxx', 'is_alpha': True}], 'deps': [{'root_head_text': 'is', 'text': 'He', 'root_text': 'He', 'root_dep': 'nsubj'}], 'ners': []}]


def test_api_math():
    assert json.loads(API.math("How much is 12 + 14?")) == '12 + 14 = 26'


def test_api_omni():
    assert json.loads(API.omni("Where is the Times Square?", "sir")) == 'New York City'


def test_api_deep():
    assert json.loads(API.deep("Do you like to listen music?", "sir")) == 'Of course.'


def test_api_wikipedia():
    assert json.loads(API.wikipedia("Albert Einstein", "sir")) == {'url': 'https://en.wikipedia.org/wiki/Albert_Einstein', 'response': 'Albert Einstein ; 14 March 1879   18 April 1955) was a German-born theoretical physicist who developed the theory of relativity, one of the two pillars of modern physics . His work is also known for its influence on the philosophy of science. He is best known to the general public for his mass energy equivalence formula E = mc2, which has been dubbed "the world\'s most famous equation".'}


def test_api_youtube():
    assert json.loads(API.youtube("Turn Down for What", "sir")) == {'url': 'https://www.youtube.com/watch?v=HMUDVMiITOU', 'response': 'DJ Snake, Lil Jon - Turn Down for What'}
