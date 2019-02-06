#!/usr/bin/python3
# -*- coding: utf-8 -*-

"""
.. module:: check_todo_compare1
    :platform: Unix
    :synopsis: the top-level submodule of Dragonfire.commands.take_note that contains the function related to Dragonfire's simple if-else struct of 1. compare of creating to do list in taking note ability.

.. moduleauthor:: Cem Baybars GÜÇLÜ <cem.baybars@gmail.com>
"""
import datetime  # Basic date and time types
from random import choice  # Generate pseudo-random numbers
from dragonfire.nlplib import Classifier, Helper  # Submodule of Dragonfire to handle extra NLP tasks

import spacy  # Industrial-strength Natural Language Processing in Python

nlp = spacy.load('en')  # Load en_core_web_sm, English, 50 MB, default model


def is_todo(com, note_taker, user_answering_note, userin, user_prefix):
    """Method to dragonfire's first command struct of taking note ability.

    Args:
        com (str):                 User's command.
        note_taker (object):        note_taker class's object.
        user_answering_note:       User answering string array.
        userin:                    :class:`dragonfire.utilities.TextToAction` instance.
        user_prefix:               user's preferred titles.
    """

    if user_answering_note['isTodo']:
        if not user_answering_note['toDo_listname']:
            user_answering_note['toDo_listname'] = com
            if not user_answering_note['note_keeper']:  # keeper compare for the elastic usage.
                return userin.say("I get it. Enter the 1. item...")
            else:
                note_taker.db_upsert(user_answering_note['note_keeper'], None, None,
                                     user_answering_note['toDo_listname'],
                                     user_answering_note['toDo_listcount'], user_answering_note['isTodo'])
                return userin.say(
                    "I get it. Enter the " + str(user_answering_note['toDo_listcount'] + 1) + ". item...")
        else:
            if com.startswith("enough") or com.startswith("it is okay") or com.startswith(
                    "it is ok") or com.startswith("it's okay") or com.startswith("it's ok") or com.startswith(
                    "end") or com.startswith(
                    "ENOUGH") or com.startswith("IT IS OKAY") or com.startswith("IT IS OK") or com.startswith(
                    "IT'S OKAY") or com.startswith("IT'S OK") or com.startswith("END"):
                temporary_keeper = user_answering_note['toDo_listname']
                user_answering_note['status'] = False
                user_answering_note['isTodo'] = False
                user_answering_note['toDo_listname'] = None
                user_answering_note['toDo_listcount'] = 0
                user_answering_note['note_keeper'] = None

                return userin.say(choice(
                    ["List was recorded", temporary_keeper + " ToDo List generated",
                     "Get it. List ready"]) + choice([".", ", " + user_prefix + "."]))
            user_answering_note['toDo_listcount'] += 1
            note_taker.db_upsert(com, None, None, user_answering_note['toDo_listname'],
                                 user_answering_note['toDo_listcount'], user_answering_note['isTodo'])

            return userin.say(choice(
                ["It is Okay. Give " + str(user_answering_note['toDo_listcount'] + 1) + ". item",
                 "Get it. Give other item", "Okay. Enter other one", "Okay, you can say other",
                 "Get it. Listening for other"]) + choice([".", ", " + user_prefix + "."]))
    return None


def is_reminder(com, h, doc, note_taker, user_answering_note, userin, user_prefix):
    """Method to dragonfire's first command struct of taking note ability.

    Args:
        com (str):                 User's command.
        note_taker (object):        note_taker class's object.
        user_answering_note:       User answering string array.
        userin:                    :class:`dragonfire.utilities.TextToAction` instance.
        user_prefix:               user's preferred titles.
    """

    if user_answering_note['isRemind']:
        if user_answering_note['is_again']:  # for using same reminder on different time.
            user_answering_note['is_again'] = False
            if com.startswith("yes") and com.endswith("yes") or com.startswith("yep") and com.endswith("yep") or com.startswith("okay") and com.endswith("okay") or h.check_deps_contains("do it"):
                return userin.say(choice(["It's okay", "Get it", "reminder will repeat", " It has been set again"]) + choice(
                    [", " + user_prefix + ". ", ". "]) + choice(
                    ["What is the remind time?", "When do you want to remind?", "Give remind time.",
                     "Say the time"]))
            else:
                return userin.say(choice(["As you wish", "I understand", "Alright", "Ready whenever you want", "Get it"]) + choice([". ", ", " + user_prefix + ". "]))

        if not user_answering_note['note_keeper']:
            user_answering_note['note_keeper'] = com
            return userin.say(choice(["It's okay", "Get it", "note was recorded", "The note taken"]) + choice(
                [", " + user_prefix + ". ", ". "]) + choice(
                ["What is the remind time?", "When do you want to remind?", "Give the remind time.",
                 "Say the time"]))
        else:  # flexible usage is going to be set.
            if com.startswith("after") or com.endswith("later") or com.startswith("in") or com.startswith(""):
                if h.check_noun_lemma("minute") or h.check_noun_lemma("minutes"):
                    takenote_query = ""
                    for token in doc:
                        if not (
                                token.lemma_ == "after" or token.lemma_ == "later" or token.lemma_ == "minute" or token.lemma_ ==
                                "minutes" or token.is_stop):
                            takenote_query += ' ' + token.text
                            mnt = float(takenote_query)
                            if is_float(mnt):
                                # timestamp is a kind of second.
                                time = datetime.datetime.now().timestamp() + mnt * 60
                                time = int(time / 60)
                                note_taker.db_upsert(user_answering_note['note_keeper'], None, time, None, None, False, True)
                                # return userin.say(str(time.strftime("%H:%M")))
                            else:
                                return userin.say("Repeat!")
                elif h.check_noun_lemma("hour") or h.check_noun_lemma("hours"):
                    takenote_query = ""
                    for token in doc:
                        if not (
                                token.lemma_ == "after" or token.lemma_ == "later" or token.lemma_ == "hour" or token.lemma_ ==
                                "hours" or token.is_stop):
                            takenote_query += ' ' + token.text
                            hr = int(takenote_query)
                            if is_float(hr):
                                # timestamp is a kind of second.
                                time = datetime.datetime.now().timestamp() + hr * 60 * 60
                                time = int(time / 60)
                                note_taker.db_upsert(user_answering_note['note_keeper'], None, time, None, None, False, True)
                                # return userin.say(str(time))
                            else:
                                return userin.say("Repeat!")
                elif h.check_noun_lemma("day") or h.check_noun_lemma("days"):
                    takenote_query = ""
                    for token in doc:
                        if not (
                                token.lemma_ == "after" or token.lemma_ == "later" or token.lemma_ == "day" or token.lemma_ ==
                                "days" or token.is_stop):
                            takenote_query += ' ' + token.text
                            dy = int(takenote_query)
                            if is_float(dy):
                                # timestamp is a kind of second.
                                time = datetime.datetime.now().timestamp() + dy * 24 * 60 * 60
                                time = int(time / 60)
                                note_taker.db_upsert(user_answering_note['note_keeper'], None, time, None, None, False, True)
                                # return userin.say(str(time))
                            else:
                                return userin.say("Repeat!")
                user_answering_note['status'] = False
                user_answering_note['isRemind'] = False
                user_answering_note['note_keeper'] = None
                return userin.say(choice(["It's okay", "Get it", "note was recorded", "The note taken"]) + choice(
                    [", " + user_prefix + ". ", ". "]) + choice(
                    ["Reminder Added.", "I'm waiting to remind.", "I will remind.",
                     "Reminder has been set."]))
    return None


def is_float(value):
    """Method to dragonfire's checking float various struct of taking reminder note ability.

            Args:
                value:     expect float.
            """
    try:
        float(value)
        return True
    except:
        return False
