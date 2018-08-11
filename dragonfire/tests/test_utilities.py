# -*- coding: utf-8 -*-

"""
.. module:: test_utilities
    :platform: Unix
    :synopsis: tests for the utilities submodule.

.. moduleauthor:: Mehmet Mert Yıldıran <mert.yildiran@bil.omu.edu.tr>
"""

from dragonfire.utilities import TextToAction

import pytest


@pytest.fixture
def userin():
    '''Returns a :class:`dragonfire.utilities.TextToAction` instance.'''

    args = {}
    args["cli"] = True
    args["silent"] = True
    args["headless"] = True
    args["verbose"] = False
    args["gspeech"] = False
    args["server"] = False
    args["port"] = 3301
    args["version"] = False
    return TextToAction(args, testing=True)


def test_utilities_say(userin):
    assert userin.say("Hello world!") == "Hello world!"
