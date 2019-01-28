#!/usr/bin/python3
# -*- coding: utf-8 -*-

"""
.. module:: takenote
    :platform: Unix
    :synopsis: the top-level submodule of Dragonfire.commands that contains the classes related to Dragonfire's simple if-else struct of taking note ability.

.. moduleauthor:: Cem Baybars GÜÇLÜ <cem.baybars@gmail.com>
"""

from random import choice  # Generate pseudo-random numbers
from dragonfire.nlplib import Classifier, Helper  # Submodule of Dragonfire to handle extra NLP tasks
from dragonfire.utilities import TextToAction, nostdout, \
    nostderr  # Submodule of Dragonfire to provide various utilities

import spacy  # Industrial-strength Natural Language Processing in Python

nlp = spacy.load('en')  # Load en_core_web_sm, English, 50 MB, default model

class TakeNoteCommand():
    """Class to contains taking notes process with simply if-else struct.
    """

    def first_compare(self, com, noteTaker, USER_ANSWERING_NOTE, userin, user_prefix):
        """Method to dragonfire's first command struct of taking note ability.

        Args:
            com (str):                 User's command.
            noteTaker (object):        NoteTaker class's object.
            USER_ANSWERING_NOTE:       User answering string array.
            userin:                    :class:`dragonfire.utilities.TextToAction` instance.
            user_prefix:               user's preferred titles.
        """

        doc = nlp(com)
        h = Helper(doc)
        if h.check_verb_lemma("add") or h.check_verb_lemma("generate") or h.check_verb_lemma(
                "create") or (
                h.check_verb_lemma("take") and h.check_noun_lemma("note")) or h.check_verb_lemma("remind"):
            if h.check_verb_lemma("do") or (                                                # FOR creating To Do list
                    h.check_verb_lemma("do") and h.check_noun_lemma("list")):
                takenote_query = ""
                for token in doc:
                    if not (
                            token.lemma_ == "add" or token.lemma_ == "generate" or token.lemma_ == "create" or
                            token.lemma_ == "do" or token.lemma_ == "list" or token.lemma_ == "dragonfire" or token.is_stop):
                        takenote_query += ' ' + token.text
                takenote_query = takenote_query.strip()
                USER_ANSWERING_NOTE['status'] = True
                USER_ANSWERING_NOTE['isTodo'] = True
                if not takenote_query:  # when command come without note.
                    return userin.say(choice([
                        "Okay, " + user_prefix + ". What is the name?",
                        "I'm listening for give a name to list, " + user_prefix + ".",
                        "Alright, " + user_prefix + ". Please, say a list name.",
                        "Ready. What is the name of list?",
                        "Say a name for list."
                    ]))
                else:  # when command came with note.
                    USER_ANSWERING_NOTE['toDo_listname'] = ""
                    USER_ANSWERING_NOTE['toDo_listcount'] = 1
                    USER_ANSWERING_NOTE['note_keeper'] = takenote_query

                    return userin.say(choice([
                        "1. item receipt. Give a name to the list, " + user_prefix + "."

                    ]))

            if h.check_text("me") or h.check_noun_lemma("reminder"):       # FOR reminder
                takenote_query = ""
                for token in doc:
                    if not (
                            token.lemma_ == "add" or token.lemma_ == "generate" or token.lemma_ == "remind" or token.lemma_ == "create" or
                            token.lemma_ == "reminder" or token.lemma_ == "dragonfire" or token.is_stop):
                        takenote_query += ' ' + token.text
                takenote_query = takenote_query.strip()
                USER_ANSWERING_NOTE['status'] = True
                USER_ANSWERING_NOTE['isRemind'] = True
                if not takenote_query:  # when command came without note.
                    return userin.say(choice([
                        "Understood. what is note?",
                        "Yes! I'm listening the note.",
                        "Alright, " + user_prefix + ". What will I remind?",
                        "Ready to record, " + user_prefix + ". what is the note?",
                        "Okay, " + user_prefix + ". Please enter the note."
                    ]))
                else:  # when command came with note.
                    USER_ANSWERING_NOTE['note_keeper'] = takenote_query
                    return userin.say(choice([
                        "It's Okay, " + user_prefix + ". When will I remind?",
                        "Alright. what do you want to remember?",
                        "Alright, " + user_prefix + ". What is the remind time?",
                        "Note taken. Give the remind time.",
                        "I get it, " + user_prefix + ". Please enter the remind time."
                    ]))

            if h.check_noun_lemma("note") or not h.check_noun_lemma(""):                    # FOR taking note.
                takenote_query = ""
                for token in doc:
                    if not (
                            token.lemma_ == "add" or token.lemma_ == "take" or token.lemma_ == "note" or token.lemma_ == "create" or
                            token.lemma_ == "generate" or token.lemma_ == "dragonfire" or token.is_stop):
                        takenote_query += ' ' + token.text
                takenote_query = takenote_query.strip()
                if not takenote_query:  # when command came without note.
                    USER_ANSWERING_NOTE['status'] = True
                    return userin.say(choice([
                        "Yes, " + user_prefix + ".",
                        "Yes. I'm listening",
                        "Alright, " + user_prefix + ".",
                        "Ready to record, " + user_prefix + ".",
                        "Keep going, " + user_prefix + "."
                    ]))
                else:  # when command came with note.
                    noteTaker.db_upsert(takenote_query)
                    USER_ANSWERING_NOTE['status'] = False
                    return userin.say(choice(["The note taken", "The note was recorded", "I get it"]) + choice(
                        [".", ", " + user_prefix + "."]))
    def second_compare(self, com, noteTaker, USER_ANSWERING_NOTE, userin, user_prefix):
        """Method to dragonfire's first command struct of taking note ability.

        Args:
            com (str):                 User's command.
            noteTaker (object):        NoteTaker class's object.
            USER_ANSWERING_NOTE:       User answering string array.
            userin:                    :class:`dragonfire.utilities.TextToAction` instance.
            user_prefix:               user's preferred titles.
        """

        if USER_ANSWERING_NOTE['status']:
            # USER_ANSWERING_NOTE['status'] = False
            if com.startswith("whatever") or com.startswith("give up") or com.startswith("not now") or com.startswith(
                    "WHATEVER") or com.startswith("GIVE UP") or com.startswith("NOT NOW"):  # for writing interrupr while taking notes and creating reminders.
                USER_ANSWERING_NOTE['status'] = False
                USER_ANSWERING_NOTE['isTodo'] = False
                USER_ANSWERING_NOTE['toDo_listname'] = None
                USER_ANSWERING_NOTE['toDo_listcount'] = 0
                USER_ANSWERING_NOTE['note_keeper'] = None
                USER_ANSWERING_NOTE['isRemind'] = False
                return userin.say(
                    choice(["As you wish", "I understand", "Alright", "Ready whenever you want", "Get it"]) + choice(
                        [". ", ", " + user_prefix + ". "]))

            if USER_ANSWERING_NOTE['isTodo']:
                if not USER_ANSWERING_NOTE['toDo_listname']:
                    USER_ANSWERING_NOTE['toDo_listname'] = com
                    if not USER_ANSWERING_NOTE['note_keeper']:  # keeper compare for the elastic usage.
                        return userin.say("I get it. Enter the 1. item...")
                    else:
                        noteTaker.db_upsert(USER_ANSWERING_NOTE['note_keeper'], None, None,
                                            USER_ANSWERING_NOTE['toDo_listname'],
                                            USER_ANSWERING_NOTE['toDo_listcount'], USER_ANSWERING_NOTE['isTodo'])
                        return userin.say(
                            "I get it. Enter the " + str(USER_ANSWERING_NOTE['toDo_listcount'] + 1) + ". item...")
                else:
                    if com.startswith("enough") or com.startswith("it is okay") or com.startswith(
                            "it is ok") or com.startswith("it's okay") or com.startswith("it's ok") or com.startswith(
                            "end") or com.startswith(
                            "ENOUGH") or com.startswith("IT IS OKAY") or com.startswith("IT IS OK") or com.startswith(
                            "IT'S OKAY") or com.startswith("IT'S OK") or com.startswith("END"):
                        temporaryKeeper = USER_ANSWERING_NOTE['toDo_listname']
                        USER_ANSWERING_NOTE['status'] = False
                        USER_ANSWERING_NOTE['isTodo'] = False
                        USER_ANSWERING_NOTE['toDo_listname'] = None
                        USER_ANSWERING_NOTE['toDo_listcount'] = 0
                        USER_ANSWERING_NOTE['note_keeper'] = None

                        return userin.say(choice(
                            ["List was recorded", temporaryKeeper + " ToDo List generated",
                             "Get it. List ready"]) + choice([".", ", " + user_prefix + "."]))
                    USER_ANSWERING_NOTE['toDo_listcount'] += 1
                    noteTaker.db_upsert(com, None, None, USER_ANSWERING_NOTE['toDo_listname'],
                                        USER_ANSWERING_NOTE['toDo_listcount'], USER_ANSWERING_NOTE['isTodo'])

                    return userin.say(choice(
                        ["It is Okay. Give " + str(USER_ANSWERING_NOTE['toDo_listcount']+1) + ". item",
                         "Get it. Give other item", "Okay. Enter other one", "Okay, you can say other",
                         "Get it. Listening for other"]) + choice([".", ", " + user_prefix + "."]))

            if USER_ANSWERING_NOTE['isRemind']:
                if not USER_ANSWERING_NOTE['note_keeper']:
                    USER_ANSWERING_NOTE['note_keeper'] = com
                    return userin.say(choice(["It's okay", "Get it", "note was recorded", "The note taken"]) + choice(
                        [", " + user_prefix + ". ", ". "]) + choice(
                        ["What is the remind time?", "When do you want to remind?", "Give remind time.",
                         "Say the time"]))
                else:
                    # Time parsing processes wil be here.
                    USER_ANSWERING_NOTE['status'] = False
                    USER_ANSWERING_NOTE['isRemind'] = False
                    USER_ANSWERING_NOTE['note_keeper'] = None
                    return userin.say(choice(["It's okay", "Get it", "note was recorded", "The note taken"]) + choice(
                        [", " + user_prefix + ". ", ". "]) + choice(
                        ["Reminder Added.", "I'm waiting to remind.", "I will remind.",
                         "Reminder has been set."]))

            else:
                USER_ANSWERING_NOTE['status'] = False
                noteTaker.db_upsert(com)
                return userin.say(choice(
                    ["The note Taken", "Alright", "I understand", "Ready whenever you want", "Get it"]) + choice(
                    [".", ", " + user_prefix + ". "]))
