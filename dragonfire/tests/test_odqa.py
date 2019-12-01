# -*- coding: utf-8 -*-

"""
.. module:: test_odqa
    :platform: Unix
    :synopsis: tests for the odqa submodule.

.. moduleauthor:: Mehmet Mert Yıldıran <mert.yildiran@bil.omu.edu.tr>
"""

from dragonfire.odqa import ODQA

import spacy
import pytest


@pytest.fixture
def odqa():
    '''Returns a :class:`dragonfire.odqa.ODQA` instance.'''

    return ODQA(spacy.load('en'))


@pytest.mark.parametrize("question, answers", [
    ("Where is Burj Khalifa?", ["Dubai, United Arab Emirates"]),
    ("What is the height of Great Pyramid of Giza?", ["146.5 metres"]),
    ("What is the atomic number of Oxygen?", ["8"]),
    ("What is the capital of Germany?", ["Berlin"]),
    ("What is the largest city of Turkey?", ["Istanbul"]),
    ("Who invented General Relativity?", ["Albert Einstein"]),
])
def test_odqa_respond(odqa, question, answers):
    assert odqa.respond(question, user_prefix="sir") in answers


def test_phrase_cleaner(odqa):
    assert odqa.phrase_cleaner("modern, physics") == "modern physics"


def test_semantic_extractor(odqa):
    assert odqa.semantic_extractor("What is the real name of Iron Man") == ('Iron Man', ['the real name'], 'real name', 'the real name Iron Man')
