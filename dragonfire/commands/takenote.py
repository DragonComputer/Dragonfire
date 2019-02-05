#!/usr/bin/python3
# -*- coding: utf-8 -*-

"""
.. module:: takenote
    :platform: Unix
    :synopsis: the top-level submodule of Dragonfire.commands that contains the classes related to Dragonfire's simple if-else struct of taking note ability.

.. moduleauthor:: Cem Baybars GÜÇLÜ <cem.baybars@gmail.com>
"""
import datetime  # Basic date and time types
from random import choice  # Generate pseudo-random numbers
from dragonfire.nlplib import Classifier, Helper  # Submodule of Dragonfire to handle extra NLP tasks

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
            if h.check_verb_lemma("do") or (                                                # FOR creating To Do list
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

            if h.check_text("me") or h.check_noun_lemma("reminder"):       # FOR reminder
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

            if h.check_noun_lemma("note") or not h.check_noun_lemma(""):                    # FOR taking note.
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
            if com.startswith("whatever") or com.startswith("give up") or com.startswith("not now") or com.startswith("WHATEVER") or com.startswith("GIVE UP") or com.startswith("NOT NOW"):  # for writing interrupr while taking notes and creating reminders.
                user_answering_note['status'] = False
                user_answering_note['isTodo'] = False
                user_answering_note['toDo_listname'] = None
                user_answering_note['toDo_listcount'] = 0
                user_answering_note['note_keeper'] = None
                user_answering_note['isRemind'] = False
                return userin.say(
                    choice(["As you wish", "I understand", "Alright", "Ready whenever you want", "Get it"]) + choice([". ", ", " + user_prefix + ". "]))

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
                        ["It is Okay. Give " + str(user_answering_note['toDo_listcount']+1) + ". item",
                         "Get it. Give other item", "Okay. Enter other one", "Okay, you can say other",
                         "Get it. Listening for other"]) + choice([".", ", " + user_prefix + "."]))

            if user_answering_note['isRemind']:
                if user_answering_note['is_again']:                # for using same reminder on different time.
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
                                    if self.is_float(mnt):
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
                                    if self.is_float(hr):
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
                                    if self.is_float(dy):
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

            else:
                user_answering_note['status'] = False
                note_taker.db_upsert(com)
                return userin.say(choice(
                    ["The note Taken", "Alright", "I understand", "Ready whenever you want", "Get it"]) + choice(
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

    def is_float(self, value):
        """Method to dragonfire's checking float various struct of taking reminder note ability.

                Args:
                    value:     expect float.
                """
        try:
            float(value)
            return True
        except:
            return False





