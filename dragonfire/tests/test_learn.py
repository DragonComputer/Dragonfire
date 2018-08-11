# -*- coding: utf-8 -*-

"""
.. module:: test_learn
    :platform: Unix
    :synopsis: tests for the learn submodule.

.. moduleauthor:: Mehmet Mert Yıldıran <mert.yildiran@bil.omu.edu.tr>
"""

import os
from os.path import expanduser

from dragonfire.learn import Learner

import spacy
import pytest


home = expanduser("~")  # Get the home directory of the user
if os.path.exists(home + '/.dragonfire_db.json'):
    os.remove(home + '/.dragonfire_db.json')  # This is where we store the database; /home/USERNAME/.dragonfire_db.json


@pytest.fixture
def learner():
    '''Returns a :class:`dragonfire.learn.Learner` instance.'''

    return Learner(spacy.load('en'))


@pytest.mark.parametrize("command, response", [
    ("the Sun is hot", "OK, I get it. the Sun is hot"),
    ("the Sun is yellow", "OK, I get it. the Sun is yellow"),
    ("Describe the Sun", "the Sun is hot and yellow"),
    ("What is the Sun", "the Sun is hot and yellow"),
    ("my age is 25", "OK, I get it. your age is 25"),
    ("What is my age", "your age is 25"),
    ("forget my age", "OK, I forgot everything I know about your age"),
    ("update my age", "I don't even know anything about your age"),
    ("my place of birth is Turkey", "OK, I get it. your place of birth is Turkey"),
    ("Where is my place of birth", "your place of birth is Turkey"),
    ("mine is golden", "OK, I get it. yours is golden"),
    ("how is mine", "yours is golden"),
    ("Albert Einstein is a Physicist", "OK, I get it. Albert Einstein is a Physicist"),
    ("Who is a Physicist", "Albert Einstein is a Physicist"),
    ("Are you evil", "")
])
def test_learner_respond(learner, command, response):
    assert learner.respond(command) == response


def test_learner_mirror(learner):
    assert learner.mirror("I'm the master") == "you are the master"
    assert learner.mirror("you are the master") == "I am the master"


def test_learner_fix_pronoun(learner):
    assert learner.fix_pronoun("yourself") == "you"


def test_learner_detect_pronoun(learner):
    assert learner.detect_pronoun("my car") == ("my car", False)
    assert learner.detect_pronoun("beautiful car") == ("beautiful car", True)


def test_learner_upper_capitalize(learner):
    assert learner.upper_capitalize(["word"]) == ["word", "Word", "WORD"]
