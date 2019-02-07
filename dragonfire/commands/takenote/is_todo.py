#!/usr/bin/python3
# -*- coding: utf-8 -*-

"""
.. module:: is_todo
    :platform: Unix
    :synopsis: the top-level submodule of Dragonfire.commands.takenote that contains the class related to Dragonfire's simple if-else struct of create to do list of taking note ability.

.. moduleauthor:: Cem Baybars GÜÇLÜ <cem.baybars@gmail.com>
"""

from random import choice  # Generate pseudo-random numbers

import spacy  # Industrial-strength Natural Language Processing in Python

nlp = spacy.load('en')  # Load en_core_web_sm, English, 50 MB, default model


class IsToDo():
    """Class to contains checking to do list part of taking notes process with simply if-else struct.
    """

    def compare1(self, h, doc, note_taker, user_answering_note, userin, user_prefix):
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

    def compare2(self, com, note_taker, user_answering_note, userin, user_prefix):
        """Method to dragonfire's second command struct for checking to do list of taking note ability.

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
