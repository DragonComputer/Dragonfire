# -*- coding: utf-8 -*-

"""
.. module:: test_dragonfire_takenote
    :platform: Unix
    :synopsis: test module for the submodule of Dragonfire, dragonfire.commands.takenote.

.. moduleauthor:: Cem Baybars GÜÇLÜ <cem.baybars@gmail.com>
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

take_note_cancel_answers = [
    "As you wish.", "I understand.", "Alright.",
    "Ready whenever you want.", "Get it.",
    "As you wish" + ", " + user_prefix + ".",
    "I understand" + ", " + user_prefix + ".",
    "Alright" + ", " + user_prefix + ".",
    "Ready whenever you want" + ", " + user_prefix + ".",
    "Get it" + ", " + user_prefix + "."
]

take_note_answers = [
    "Yes, " + user_prefix + ".",
    "Yes. I'm listening",
    "Alright, " + user_prefix + ".",
    "Ready to record, " + user_prefix + ".",
    "Keep going, " + user_prefix + "."
]

create_todo_list_answers = [
    "Okay, " + user_prefix + ". What is the name?",
    "I'm listening for give a name to list, " + user_prefix + ".",
    "Alright, " + user_prefix + ". Please, say a list name.",
    "Ready. What is the name of list?",
    "Say a name for list."
]

create_reminder_answers = [
    "Understood. what is note?",
    "Yes! I'm listening the note.",
    "Alright, " + user_prefix + ". What will I remind?",
    "Ready to record, " + user_prefix + ". what is the note?",
    "Okay, " + user_prefix + ". Please enter the note."
]

create_reminder_answers2 = [
    "It's Okay, " + user_prefix + ". When will I remind?",
    "Alright. When do you want to remember?",
    "Alright, " + user_prefix + ". What is the remind time?",
    "Note taken. Give the remind time.",
    "I get it, " + user_prefix + ". Please enter the remind time."
]


@pytest.fixture
def virtual_assistant():
    """Returns a :class:`dragonfire.VirtualAssistant` instance."""

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


def test_take_note_compare(virtual_assistant):

    assert virtual_assistant.command("hey") in hey_answers
    assert virtual_assistant.command("take note") in take_note_answers
    assert virtual_assistant.command("whatever") in take_note_cancel_answers
    assert virtual_assistant.command("create to do list") in create_todo_list_answers
    assert virtual_assistant.command("forget it") in take_note_cancel_answers
    assert virtual_assistant.command("remind me") in create_reminder_answers
    assert virtual_assistant.command("give up") in take_note_cancel_answers
    assert virtual_assistant.command("this is sample of reminder note. remind me this note.") in create_reminder_answers2
    assert virtual_assistant.command("give up") in take_note_cancel_answers




