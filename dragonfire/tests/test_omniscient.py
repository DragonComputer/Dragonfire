# -*- coding: utf-8 -*-

"""
.. module:: test_omniscient
    :platform: Unix
    :synopsis: tests for the omniscient submodule.

.. moduleauthor:: Mehmet Mert Yıldıran <mert.yildiran@bil.omu.edu.tr>
"""

from dragonfire.omniscient import Omniscient

import spacy
import pytest


@pytest.fixture
def omniscient():
    '''Returns a :class:`dragonfire.omniscient.Omniscient` instance.'''

    return Omniscient(spacy.load('en'))


@pytest.mark.parametrize("question, answers", [
    ("Where is the Times Square", ["New York City", "\n"]),
    ("What is the height of Burj Khalifa", ["828 m"]),
    ("What is the real name of Iron Man", ["Tony", "Stark", "Tony Stark"]),
    ("When Constantinople was conquered", ["1453"]),
    ("What is the name of the world's longest river", ["Nile", "Amazon"])
])
def test_omniscient_respond(omniscient, question, answers):
    assert omniscient.respond(question, user_prefix="sir") in answers


def test_wordnet_entity_determiner(omniscient):
    assert omniscient.wordnet_entity_determiner("Luther", False, False) == ['PERSON']


def test_phrase_cleaner(omniscient):
    assert omniscient.phrase_cleaner("modern, physics") == "modern physics"


def test_semantic_extractor(omniscient):
    assert omniscient.semantic_extractor("What is the real name of Iron Man") == ('Iron Man', ['the real name'], 'real name', 'the real name Iron Man')
