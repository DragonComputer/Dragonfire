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
    ("Where is Burj Khalifa?", ["Dubai, United Arab Emirates"]),
    ("What is the height of Great Pyramid of Giza?", ["146.5 metres"]),
    ("What is the atomic number of Oxygen?", ["8"]),
    ("What is the capital of Germany?", ["Berlin"]),
    ("What is the largest city of Turkey?", ["Istanbul"]),
    ("Who invented General Relativity?", ["Albert Einstein"]),
])
def test_omniscient_respond(omniscient, question, answers):
    assert omniscient.respond(question, user_prefix="sir") in answers


def test_phrase_cleaner(omniscient):
    assert omniscient.phrase_cleaner("modern, physics") == "modern physics"


def test_semantic_extractor(omniscient):
    assert omniscient.semantic_extractor("What is the real name of Iron Man") == ('Iron Man', ['the real name'], 'real name', 'the real name Iron Man')
