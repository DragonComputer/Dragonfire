#!/usr/bin/python3
# -*- coding: utf-8 -*-

"""
.. module:: check_take_compare1
    :platform: Unix
    :synopsis: the top-level submodule of Dragonfire.commands.takenote_submodules that contains the function related to Dragonfire's simple if-else struct of taking note ability.

.. moduleauthor:: Cem Baybars GÜÇLÜ <cem.baybars@gmail.com>
"""
import datetime  # Basic date and time types
from random import choice  # Generate pseudo-random numbers
from dragonfire.nlplib import Classifier, Helper  # Submodule of Dragonfire to handle extra NLP tasks

import spacy  # Industrial-strength Natural Language Processing in Python

nlp = spacy.load('en')  # Load en_core_web_sm, English, 50 MB, default model


def is_todo(h, doc, note_taker, user_answering_note, userin, user_prefix):
    """Method to dragonfire's first command struct for checking to do list of taking note ability.

    Args:
        h:                          doc's helper.
        doc:                        object with nlp from user answering to doc.
        note_taker (object):        note_taker class's object.
        user_answering_note:       User answering string array.
        userin:                    :class:`dragonfire.utilities.TextToAction` instance.
        user_prefix:               user's preferred titles.
    """

    if h.check_verb_lemma("do") or (  # FOR creating To Do list
            h.check_verb_lemma("do") and h.check_noun_lemma("list")):
        takenote_query = ""
        for token in doc:
            if not (
                    token.lemma_ == "add" or token.lemma_ == "generate" or token.lemma_ == "create" or
                    token.lemma_ == "do" or token.lemma_ == "list" or token.lemma_ == "dragonfire" or token.is_stop):
                takenote_query += ' ' + token.text
        takenote_query = takenote_query.strip()
        user_answering_note['status'] = True
        user_answering_note['isTodo'] = True
        if not takenote_query:  # when command come without note.
            return userin.say(choice([
                "Okay, " + user_prefix + ". What is the name?",
                "I'm listening for give a name to list, " + user_prefix + ".",
                "Alright, " + user_prefix + ". Please, say a list name.",
                "Ready. What is the name of list?",
                "Say a name for list."
            ]))
        else:  # when command came with note.
            user_answering_note['toDo_listname'] = ""
            user_answering_note['toDo_listcount'] = 1
            user_answering_note['note_keeper'] = takenote_query

            return userin.say(choice([
                "1. item receipt. Give a name to the list, " + user_prefix + "."

            ]))
    return None


def is_reminder(h, doc, note_taker, user_answering_note, userin, user_prefix):
    """Method to dragonfire's first command struct for checking reminder of taking note ability.

    Args:
        h:                          doc's helper.
        doc:                        object with nlp from user answering to doc.
        note_taker (object):        note_taker class's object.
        user_answering_note:       User answering string array.
        userin:                    :class:`dragonfire.utilities.TextToAction` instance.
        user_prefix:               user's preferred titles.
    """

    if h.check_text("me") or h.check_noun_lemma("reminder"):  # FOR reminder
        takenote_query = ""
        for token in doc:
            if not (
                    token.lemma_ == "add" or token.lemma_ == "generate" or token.lemma_ == "remind" or token.lemma_ == "create" or
                    token.lemma_ == "reminder" or token.lemma_ == "dragonfire" or token.is_stop):
                takenote_query += ' ' + token.text
        takenote_query = takenote_query.strip()
        user_answering_note['status'] = True
        user_answering_note['isRemind'] = True
        if not takenote_query:  # when command came without note.
            return userin.say(choice([
                "Understood. what is note?",
                "Yes! I'm listening the note.",
                "Alright, " + user_prefix + ". What will I remind?",
                "Ready to record, " + user_prefix + ". what is the note?",
                "Okay, " + user_prefix + ". Please enter the note."
            ]))
        else:  # when command came with note.
            user_answering_note['note_keeper'] = takenote_query
            return userin.say(choice([
                "It's Okay, " + user_prefix + ". When will I remind?",
                "Alright. When do you want to remember?",
                "Alright, " + user_prefix + ". What is the remind time?",
                "Note taken. Give the remind time.",
                "I get it, " + user_prefix + ". Please enter the remind time."
            ]))
    return None


def is_note(h, doc, note_taker, user_answering_note, userin, user_prefix):
    """Method to dragonfire's first command struct for checking note of taking note ability.

    Args:
        h:                          doc's helper.
        doc:                        object with nlp from user answering to doc.
        note_taker (object):        note_taker class's object.
        user_answering_note:       User answering string array.
        userin:                    :class:`dragonfire.utilities.TextToAction` instance.
        user_prefix:               user's preferred titles.
    """

    if h.check_noun_lemma("note") or not h.check_noun_lemma(""):  # FOR taking note.
        takenote_query = ""
        for token in doc:
            if not (
                    token.lemma_ == "add" or token.lemma_ == "take" or token.lemma_ == "note" or token.lemma_ == "create" or
                    token.lemma_ == "generate" or token.lemma_ == "dragonfire" or token.is_stop):
                takenote_query += ' ' + token.text
        takenote_query = takenote_query.strip()
        if not takenote_query:  # when command came without note.
            user_answering_note['status'] = True
            return userin.say(choice([
                "Yes, " + user_prefix + ".",
                "Yes. I'm listening",
                "Alright, " + user_prefix + ".",
                "Ready to record, " + user_prefix + ".",
                "Keep going, " + user_prefix + "."
            ]))
        else:  # when command came with note.
            note_taker.db_upsert(takenote_query)
            user_answering_note['status'] = False
            return userin.say(choice(["The note taken", "The note was recorded", "I get it"]) + choice(
                [".", ", " + user_prefix + "."]))
    return None
