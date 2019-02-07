# -*- coding: utf-8 -*-

"""
.. module:: test_take_note
    :platform: Unix
    :synopsis: tests for the take_note submodule.

.. moduleauthor:: Cem Baybars GÜÇLÜ <cem.baybars@gmail.com>
"""

import os
from os.path import expanduser

from dragonfire.takenote import NoteTaker

import pytest


home = expanduser("~")  # Get the home directory of the user
if os.path.exists(home + '/.dragonfire_db.json'):
    os.remove(home + '/.dragonfire_db.json')  # This is where we store the database; /home/USERNAME/.dragonfire_db.json


@pytest.fixture
def note_taker():
    """Returns a :class:`dragonfire.learn.NoteTaker` instance."""

    return NoteTaker()


def test_note_taker_db_get(note_taker):
    assert note_taker.db_get(None, None) == "There is no note"
