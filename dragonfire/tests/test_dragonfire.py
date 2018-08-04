#!/usr/bin/python3
# -*- coding: utf-8 -*-

"""
.. module:: text_dragonfire
    :platform: Unix
    :synopsis: test module for the top-level module of Dragonfire.

.. moduleauthor:: Mehmet Mert Yıldıran <mert.yildiran@bil.omu.edu.tr>
"""

from dragonfire import VirtualAssistant, greet
from dragonfire.utilities import TextToAction

import pytest


user_full_name = "John Doe"
user_prefix = "sir"
hey_answers = [
    "Yes, " + user_prefix + ".",
    "Yes. I'm waiting.",
    "What is your order?",
    "Ready for the orders!",
    user_prefix.capitalize() + ", tell me your wish."
]


@pytest.fixture
def virtual_assistant():
    '''Returns a :class:`dragonfire.VirtualAssistant` instance.'''

    args = {}
    args["cli"] = True
    args["silent"] = True
    args["headless"] = True
    args["verbose"] = False
    args["gspeech"] = False
    args["server"] = False
    args["port"] = 3301
    args["version"] = False
    userin = TextToAction(args, testing=True)

    return VirtualAssistant(args, userin, testing=True)


def test_builtin_commands(virtual_assistant):

    assert not virtual_assistant.command(76)
    assert virtual_assistant.command("open files") == ""

    assert virtual_assistant.command("dragonfire") in hey_answers
    assert virtual_assistant.command("dragon fire") in hey_answers
    assert virtual_assistant.command("go to sleep") == "I'm going to sleep"
    assert virtual_assistant.command("hey") in hey_answers
    assert virtual_assistant.command("stop listening") == "I'm going to sleep"
    assert virtual_assistant.command("wake up") in hey_answers

    assert virtual_assistant.command("enough") == "Dragonfire quiets."
    assert virtual_assistant.command("shut up") == "Dragonfire quiets."

    assert virtual_assistant.command("What is your name?") == "My name is Dragonfire."
    assert virtual_assistant.command("What is your gender?") == "I have a female voice but I don't have a gender identity. I'm a computer program, " + user_prefix + "."
    assert virtual_assistant.command("Who am I?") == "Your name is " + user_full_name + ", " + user_prefix + "."

    assert virtual_assistant.command("open Blender") == "Blender 3D computer graphics software"
    assert virtual_assistant.command("run draw") == "Opening LibreOffice Draw"
    assert virtual_assistant.command("open impress") == "Opening LibreOffice Impress"
    assert virtual_assistant.command("open math") == "Opening LibreOffice Math"
    assert virtual_assistant.command("open writer") == "Opening LibreOffice Writer"
    assert virtual_assistant.command("open Gimp") == "Opening the photo editor software."
    assert virtual_assistant.command("open Inkscape") == "Opening the vectorial drawing software."
    assert virtual_assistant.command("open office suite") == "Opening LibreOffice"
    assert virtual_assistant.command("run Blender") == "Blender 3D computer graphics software"
    assert virtual_assistant.command("open Kdenlive") == "Opening the video editor software."
    assert virtual_assistant.command("open browser") == "Web browser"
    assert virtual_assistant.command("start Chrome") == "Web browser"
    assert virtual_assistant.command("open Firefox") == "Web browser"
    assert virtual_assistant.command("open Steam") == "Opening Steam Game Store"
    assert virtual_assistant.command("open files") == "File Manager"
    assert virtual_assistant.command("open file manager") == "File Manager"
    assert virtual_assistant.command("open camera") == "Camera"
    assert virtual_assistant.command("open calendar") == "Calendar"
    assert virtual_assistant.command("open calculator") == "Calculator"
    assert virtual_assistant.command("open software center") == "Software Center"

    assert virtual_assistant.command("I'm a girl") == "Pardon, my lady."
    assert virtual_assistant.command("call me master") == "OK, master."
    assert virtual_assistant.command("I'm a boy") == "Pardon, sir."

    assert virtual_assistant.command("What's the temperature in New York?").startswith("The temperature in")

    assert virtual_assistant.command("keyboard blabla") == "keyboard"
    assert virtual_assistant.command("type blabla") == "keyboard"
    assert virtual_assistant.command("enter") == "enter"
    assert virtual_assistant.command("new line") == "enter"
    assert virtual_assistant.command("new tab") == "new tab"
    assert virtual_assistant.command("switch tab") == "switch tab"
    assert virtual_assistant.command("close") == "close"
    assert virtual_assistant.command("back") == "back"
    assert virtual_assistant.command("forward") == "forward"
    assert virtual_assistant.command("swipe left") == "swipe left"
    assert virtual_assistant.command("swipe right") == "swipe right"
    assert virtual_assistant.command("swipe up") == "swipe up"
    assert virtual_assistant.command("swipe down") == "swipe down"
    assert virtual_assistant.command("play") == "play"

    assert virtual_assistant.command("shut down the computer") == "Shutting down"
    assert virtual_assistant.command("power off the computer") == "Shutting down"

    assert virtual_assistant.command("goodbye") == "Goodbye, " + user_prefix
    assert virtual_assistant.command("bye") == "Goodbye, " + user_prefix
    assert virtual_assistant.command("see you later") == "Goodbye, " + user_prefix

    assert virtual_assistant.command("search Albert Einstein in Wikipedia").startswith("Albert Einstein ; 14 March 1879   18 April 1955) was a German-born theoretical physicist who developed the theory of relativity")
    assert virtual_assistant.command("find Albert Einstein on Wikipedia").startswith("Albert Einstein ; 14 March 1879   18 April 1955) was a German-born theoretical physicist who developed the theory of relativity")

    assert virtual_assistant.command("search Katy Perry in YouTube") == "Katy Perry - Roar (Official)"
    assert virtual_assistant.command("find Katy Perry on YouTube") == "Katy Perry - Roar (Official)"

    assert virtual_assistant.command("search Albert Einstein on the internet") == "Albert Einstein"
    assert virtual_assistant.command("search the images of Albert Einstein in Google images") == "Albert Einstein"


def test_arithmetic_response(virtual_assistant):

    assert virtual_assistant.command("hey") in hey_answers
    assert virtual_assistant.command("How much is 12 + 14?") == "12 + 14 = 26"
    assert virtual_assistant.command("How much is twelve thousand three hundred four plus two hundred fifty six?") == "12304 + 256 = 12560"


def test_learner_response(virtual_assistant):

    assert virtual_assistant.command("hey") in hey_answers
    assert virtual_assistant.command("the Sun is hot") == "OK, I get it. the Sun is hot"
    assert virtual_assistant.command("the Sun is yellow") == "OK, I get it. the Sun is yellow"
    assert virtual_assistant.command("Describe the Sun") == "the Sun is hot and yellow"
    assert virtual_assistant.command("What is the Sun") == "the Sun is hot and yellow"


def test_omniscient_response(virtual_assistant):

    assert virtual_assistant.command("hey") in hey_answers
    assert virtual_assistant.command("Where is the Times Square?") == "New York City"
    assert virtual_assistant.command("What is the real name of Iron Man?") in ["Tony", "Stark", "Tony Stark"]


def test_deepconv_response(virtual_assistant):

    assert virtual_assistant.command("hey") in hey_answers
    assert virtual_assistant.command("Do you like to listen music?") == "Of course."
    assert virtual_assistant.command("Are you evil?") == "Yes."
    assert virtual_assistant.command("You are so sexy") == "How do you know that?"


def test_greet(virtual_assistant):

    assert greet(virtual_assistant.userin).startswith("Good")
