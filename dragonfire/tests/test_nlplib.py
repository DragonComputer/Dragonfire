# -*- coding: utf-8 -*-

"""
.. module:: test_nlplib
    :platform: Unix
    :synopsis: tests for the nlplib submodule.

.. moduleauthor:: Mehmet Mert Yıldıran <mert.yildiran@bil.omu.edu.tr>
"""

from dragonfire.nlplib import Classifier, TopicExtractor, Helper

import spacy
import pytest


nlp = spacy.load('en')


@pytest.mark.parametrize("name, gender", [
    ("John", "male"),
    ("James", "male"),
    ("Robert", "male"),
    ("Emily", "female"),
    ("Mary", "female"),
    ("Linda", "female")
])
def test_classifier_gender(name, gender):
    assert Classifier.gender(name) == gender


@pytest.fixture
def extractor():
    '''Returns a :class:`dragonfire.nlplib.TopicExtractor` instance.'''

    return TopicExtractor()


def test_extractor_tokenize_sentence(extractor):
    assert extractor.tokenize_sentence("the Sun is hot and yellow") == ['the', 'Sun', 'is', 'hot', 'and', 'yellow']


def test_extractor_extract(extractor):
    assert extractor.extract("the Sun is hot and yellow") == ['Sun']
    assert extractor.extract("Do you know the birthdate of Barrack Obama") == ['Barrack Obama']


@pytest.fixture
def helper():
    '''Returns a :class:`dragonfire.nlplib.Helper` instance.'''

    doc = nlp("Albert Einstein was a German-born theoretical physicist who developed the theory of relativity, one of the two pillars of modern physics. His work is also known for its influence on the philosophy of science.")
    return Helper(doc)


def test_helper_directly_equal():
    doc = nlp("test")
    h = Helper(doc)
    assert h.directly_equal(["car", "test"])
    assert not h.directly_equal(["car", "building"])


def test_helper_check_nth_lemma(helper):
    h = helper
    assert h.check_nth_lemma(7, "theoretical")
    assert not h.check_nth_lemma(13, "physicist")


def test_helper_check_verb_lemma(helper):
    h = helper
    assert h.check_verb_lemma("develop")
    assert not h.check_verb_lemma("run")


def test_helper_check_wh_lemma(helper):
    doc = nlp("When was albert einstein born?")
    h = Helper(doc)
    assert h.check_wh_lemma("when")
    h = helper
    assert not h.check_wh_lemma("when")


def test_helper_check_deps_contains(helper):
    h = helper
    assert h.check_deps_contains("the two pillars")
    assert not h.check_deps_contains("particle physics")


def test_helper_check_only_dep_is(helper):
    doc = nlp("Modern physics is great!")
    h = Helper(doc)
    assert h.check_only_dep_is("modern physics")
    h = helper
    assert not h.check_only_dep_is("modern physics")


def test_helper_check_noun_lemma(helper):
    h = helper
    assert h.check_noun_lemma("physicist")
    assert not h.check_noun_lemma("soldier")


def test_helper_check_adj_lemma(helper):
    h = helper
    assert h.check_adj_lemma("theoretical")
    assert not h.check_adj_lemma("red")


def test_helper_check_adv_lemma(helper):
    h = helper
    assert h.check_adv_lemma("also")
    assert not h.check_adj_lemma("slowly")


def test_helper_check_lemma(helper):
    h = helper
    assert h.check_lemma("pillar")
    assert not h.check_lemma("car")


def test_helper_check_text(helper):
    h = helper
    assert h.check_text("Albert")
    assert not h.check_text("Robert")


def test_helper_is_wh_question(helper):
    doc = nlp("When was albert einstein born?")
    h = Helper(doc)
    assert h.is_wh_question()
    h = helper
    assert not h.is_wh_question()


def test_helper_max_word_count(helper):
    h = helper
    assert h.max_word_count(100)
    assert not h.max_word_count(5)
