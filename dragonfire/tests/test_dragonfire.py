# -*- coding: utf-8 -*-

"""
.. module:: test_dragonfire
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


@pytest.mark.parametrize("command, response", [
    (76, False),
    ("enough", "Dragonfire quiets."),
    ("shut up", "Dragonfire quiets."),
    ("What is your name?", "My name is Dragonfire."),
    ("What is your gender?", "I have a female voice but I don't have a gender identity. I'm a computer program, " + user_prefix + "."),
    ("Who am I?", "Your name is " + user_full_name + ", " + user_prefix + "."),
    ("open Blender", "Blender 3D computer graphics software"),
    ("run draw", "Opening LibreOffice Draw"),
    ("open impress", "Opening LibreOffice Impress"),
    ("open math", "Opening LibreOffice Math"),
    ("open writer", "Opening LibreOffice Writer"),
    ("open Gimp", "Opening the photo editor software."),
    ("open Inkscape", "Opening the vectorial drawing software."),
    ("open office suite", "Opening LibreOffice"),
    ("run Blender", "Blender 3D computer graphics software"),
    ("open Kdenlive", "Opening the video editor software."),
    ("open browser", "Web browser"),
    ("start Chrome", "Web browser"),
    ("open Firefox", "Web browser"),
    ("open Steam", "Opening Steam Game Store"),
    ("open files", "File Manager"),
    ("open file manager", "File Manager"),
    ("open camera", "Camera"),
    ("open calendar", "Calendar"),
    ("open calculator", "Calculator"),
    ("open software center", "Software Center"),
    ("I'm a girl", "Pardon, my lady."),
    ("call me master", "OK, master."),
    ("I'm a boy", "Pardon, sir."),
    ("keyboard blabla", "keyboard"),
    ("type blabla", "keyboard"),
    ("enter", "enter"),
    ("new line", "enter"),
    ("new tab", "new tab"),
    ("switch tab", "switch tab"),
    ("close", "close"),
    ("back", "back"),
    ("forward", "forward"),
    ("swipe left", "swipe left"),
    ("swipe right", "swipe right"),
    ("swipe up", "swipe up"),
    ("swipe down", "swipe down"),
    ("play", "play"),
    ("shut down the computer", "Shutting down"),
    ("power off the computer", "Shutting down"),
    ("goodbye", "Goodbye, " + user_prefix),
    ("bye", "Goodbye, " + user_prefix),
    ("see you later", "Goodbye, " + user_prefix),
    ("search Turn Down for What in YouTube", "DJ Snake, Lil Jon - Turn Down for What"),
    ("find Turn Down for What on YouTube", "DJ Snake, Lil Jon - Turn Down for What"),
    ("search Albert Einstein on the internet", "Albert Einstein"),
    ("search the images of Albert Einstein in Google images", "Albert Einstein")
])
def test_builtin_commands(virtual_assistant, command, response):
    assert virtual_assistant.command("hey") in hey_answers
    assert virtual_assistant.command(command) == response


def test_builtin_commands_sleep(virtual_assistant):
    assert virtual_assistant.command("open files") == ""
    assert virtual_assistant.command("dragonfire") in hey_answers
    assert virtual_assistant.command("dragon fire") in hey_answers
    assert virtual_assistant.command("go to sleep") == "I'm going to sleep"
    assert virtual_assistant.command("hey") in hey_answers
    assert virtual_assistant.command("stop listening") == "I'm going to sleep"
    assert virtual_assistant.command("wake up") in hey_answers


@pytest.mark.parametrize("command, response", [
    ("What's the temperature in New York?", "The temperature in"),
    ("search Albert Einstein in Wikipedia", "Albert Einstein ; 14 March 1879   18 April 1955) was a German-born theoretical physicist who developed the theory of relativity"),
    ("find Albert Einstein on Wikipedia", "Albert Einstein ; 14 March 1879   18 April 1955) was a German-born theoretical physicist who developed the theory of relativity")
])
def test_builtin_commands_startswith(virtual_assistant, command, response):
    assert virtual_assistant.command("hey") in hey_answers
    assert virtual_assistant.command(command).startswith(response)


def test_arithmetic_response(virtual_assistant):

    assert virtual_assistant.command("hey") in hey_answers
    assert virtual_assistant.command("How much is 12 + 14?") == "12 + 14 = 26"
    assert virtual_assistant.command("How much is twelve thousand three hundred four plus two hundred fifty six?") == "12304 + 256 = 12560"


def test_learner_response(virtual_assistant):

    assert virtual_assistant.command("hey") in hey_answers
    assert virtual_assistant.command("the Sun is hot") == "OK, I get it. the Sun is hot"
    assert virtual_assistant.command("It is yellow") == "OK, I get it. the Sun is yellow"
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
