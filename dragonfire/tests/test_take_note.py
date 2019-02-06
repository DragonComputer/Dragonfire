# -*- coding: utf-8 -*-

"""
.. module:: test_learn
    :platform: Unix
    :synopsis: tests for the learn submodule.

.. moduleauthor:: Mehmet Mert Yıldıran <mert.yildiran@bil.omu.edu.tr>
"""

import os
from os.path import expanduser

from dragonfire.take_note import NoteTaker

import spacy
import pytest


home = expanduser("~")  # Get the home directory of the user
if os.path.exists(home + '/.dragonfire_db.json'):
    os.remove(home + '/.dragonfire_db.json')  # This is where we store the database; /home/USERNAME/.dragonfire_db.json


@pytest.fixture
def note_taker():
    '''Returns a :class:`dragonfire.learn.NoteTaker` instance.'''

    return NoteTaker()


# @pytest.mark.parametrize("command, response", [
#     ("the Sun is hot", "OK, I get it. the Sun is hot"),
#     ("the Sun is yellow", "OK, I get it. the Sun is yellow"),
#     ("Describe the Sun", "the Sun is hot and yellow"),
#     ("What is the Sun", "the Sun is hot and yellow"),
#     ("my age is 25", "OK, I get it. your age is 25"),
#     ("What is my age", "your age is 25"),
#     ("forget my age", "OK, I forgot everything I know about your age"),
#     ("update my age", "I don't even know anything about your age"),
#     ("my place of birth is Turkey", "OK, I get it. your place of birth is Turkey"),
#     ("Where is my place of birth", "your place of birth is Turkey"),
#     ("mine is golden", "OK, I get it. yours is golden"),
#     ("how is mine", "yours is golden"),
#     ("Albert Einstein is a Physicist", "OK, I get it. Albert Einstein is a Physicist"),
#     ("Who is a Physicist", "Albert Einstein is a Physicist"),
#     ("Are you evil", "")
# ])
#note_taker  NoteTaker'ı return ettiği için NotaTaker'in üye fonksiyonlarını kullanacak.
# def test_note_taker_respond(note_taker, command, response):
#     assert note_taker.respond(command) == response


def test_note_taker_db_get(note_taker):
    assert note_taker.db_get(None, None) == "There is no note"
