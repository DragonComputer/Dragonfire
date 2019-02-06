#!/usr/bin/python3
# -*- coding: utf-8 -*-

"""
.. module:: take_note
    :platform: Unix
    :synopsis: the top-level submodule of Dragonfire.commands that contains the classes related to Dragonfire's simple if-else struct of taking note ability.

.. moduleauthor:: Cem Baybars GÜÇLÜ <cem.baybars@gmail.com>
"""
import datetime  # Basic date and time types
from random import choice  # Generate pseudo-random numbers
from dragonfire.nlplib import Classifier, Helper  # Submodule of Dragonfire to handle extra NLP tasks

from dragonfire.commands.take_note import check_take_compare1
from dragonfire.commands.take_note import check_take_compare2

import spacy  # Industrial-strength Natural Language Processing in Python

nlp = spacy.load('en')  # Load en_core_web_sm, English, 50 MB, default model


class TakeNoteCommand():
    """Class to contains taking notes process with simply if-else struct.
    """

    def takenote_compare1(self, com, note_taker, user_answering_note, userin, user_prefix):
        """Method to dragonfire's first command struct of taking note ability.

        Args:
            com (str):                 User's command.
            note_taker (object):        note_taker class's object.
            user_answering_note:       User answering string array.
            userin:                    :class:`dragonfire.utilities.TextToAction` instance.
            user_prefix:               user's preferred titles.
        """

        doc = nlp(com)
        h = Helper(doc)
        if h.check_verb_lemma("add") or h.check_verb_lemma("generate") or h.check_verb_lemma(
                "create") or (
                h.check_verb_lemma("take") and h.check_noun_lemma("note")) or h.check_verb_lemma("remind"):

            response = check_take_compare1.is_todo(h, doc, note_taker, user_answering_note, userin, user_prefix)   # FOR creating To Do list
            if response:
                return response

            response = check_take_compare1.is_reminder(h, doc, note_taker, user_answering_note, userin, user_prefix)  # FOR reminder
            if response:
                return response

            response = check_take_compare1.is_note(h, doc, note_taker, user_answering_note, userin, user_prefix)  # FOR taking note
            if response:
                return response

        return None

    def takenote_compare2(self, com, note_taker, user_answering_note, userin, user_prefix):
        """Method to dragonfire's first command struct of taking note ability.

        Args:
            com (str):                 User's command.
            note_taker (object):        note_taker class's object.
            user_answering_note:       User answering string array.
            userin:                    :class:`dragonfire.utilities.TextToAction` instance.
            user_prefix:               user's preferred titles.
        """
        doc = nlp(com)
        h = Helper(doc)
        if user_answering_note['status']:
            if com.startswith("whatever") or com.startswith("give up") or com.startswith("not now") or com.startswith("forget it") or com.startswith("WHATEVER") or com.startswith("GIVE UP") or com.startswith("NOT NOW") or com.startswith("FORGET IT"):  # for writing interrupt while taking notes and creating reminders.
                user_answering_note['status'] = False
                user_answering_note['isTodo'] = False
                user_answering_note['toDo_listname'] = None
                user_answering_note['toDo_listcount'] = 0
                user_answering_note['note_keeper'] = None
                user_answering_note['isRemind'] = False
                return userin.say(
                    choice(["As you wish", "I understand", "Alright", "Ready whenever you want", "Get it"]) + choice([". ", ", " + user_prefix + ". "]))

            response = check_take_compare2.is_todo(com, note_taker, user_answering_note, userin, user_prefix)  # FOR taking note
            if response:
                return response

            response = check_take_compare2.is_reminder(com, h, doc, note_taker, user_answering_note, userin, user_prefix)  # FOR taking note
            if response:
                return response

            else:                                      # taking note second compare here.
                user_answering_note['status'] = False
                note_taker.db_upsert(com)
                return userin.say(choice(
                    ["The note Taken", "Alright", "I noted", "Ready whenever you want to get it", "Get it"]) + choice(
                    [".", ", " + user_prefix + ". "]))

        return None

    def getnote_compare1(self, com, note_taker, user_answering_note, userin, user_prefix):
        """Method to dragonfire's first command struct of getting note ability.

                Args:
                    com (str):                 User's command.
                    note_taker (object):        note_taker class's object.
                    user_answering_note:       User answering string array.
                    userin:                    :class:`dragonfire.utilities.TextToAction` instance.
                    user_prefix:               user's preferred titles.
                """
        doc = nlp(com)
        h = Helper(doc)
        if h.check_verb_lemma("say") or h.check_verb_lemma("get") or h.check_verb_lemma("give"):

            if h.check_noun_lemma("note") or h.check_noun_lemma("notes"):
                return userin.say(note_taker.db_get(None, None))

            if h.check_verb_lemma("do") or (h.check_verb_lemma("do") and h.check_noun_lemma("list")):
                takenote_query = ""
                for token in doc:
                    if not (
                            token.lemma_ == "say" or token.lemma_ == "get" or token.lemma_ == "give" or
                            token.lemma_ == "do" or token.lemma_ == "list" or token.lemma_ == "dragonfire" or token.is_stop):
                        takenote_query += ' ' + token.text
                takenote_query = takenote_query.strip()
                if not takenote_query:  # when command come without note.
                    user_answering_note['has_listname'] = False
                    return userin.say(choice([
                        "which list",
                        "Alright, say a list name",
                        "Okay, What is the name of list",
                        "List name"
                    ]) + choice(["?", ", " + user_prefix + "?"]))
                else:  # when command came with note.                    # BU KISMI HALLEDECEĞİM. SİLME İŞLEMLERİ, TOPLU SİLME, İTEM SİLME,
                    result = note_taker.db_get(None, com, True)
                    if result == "*#$":
                        user_answering_note['has_listname'] = False
                        return userin.say(choice([
                            "This name is not exist",
                            "I couldn't find it, say again",
                            "Not found, Repeat",
                            "Not exist, speak again"
                        ]) + choice(["?", ", " + user_prefix + "?"]))
                    else:
                        return userin.say(note_taker.db_get(None, com, True))
        return None

    def getnote_compare2(self, com, note_taker, user_answering_note, userin, user_prefix):
        """Method to dragonfire's second command struct of getting note ability.

        Args:
            com (str):                 User's command.
            note_taker (object):        note_taker class's object.
            user_answering_note:       User answering string array.
            userin:                    :class:`dragonfire.utilities.TextToAction` instance.
            user_prefix:               user's preferred titles.
        """

        if not user_answering_note['has_listname']:
            if com.startswith("whatever") or com.startswith("give up") or com.startswith("not now") or com.startswith("WHATEVER") or com.startswith("GIVE UP") or com.startswith("NOT NOW"):  # for writing interrupr while taking notes and creating reminders.
                user_answering_note['has_listname'] = True
                return userin.say(
                    choice(["As you wish", "I understand", "Alright", "Ready whenever you want", "Get it"]) + choice(
                        [". ", ", " + user_prefix + ". "]))
            result = note_taker.db_get(None, com, True)
            if result == "*#$":
                return userin.say(choice([
                    "This name is not exist",
                    "I couldn't find it, say again",
                    "Not found, Repeat",
                    "Not exist, speak again"
                ]) + choice(["?", ", " + user_prefix + "?"]))
            else:
                user_answering_note['has_listname'] = True
                return userin.say(note_taker.db_get(None, com, True))
        return None






