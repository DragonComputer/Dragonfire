#!/usr/bin/python3
# -*- coding: utf-8 -*-

"""
.. module:: is_treminder
    :platform: Unix
    :synopsis: the top-level submodule of Dragonfire.commands.takenote that contains the class related to Dragonfire's simple if-else struct of create reminder of taking note ability.

.. moduleauthor:: Cem Baybars GÜÇLÜ <cem.baybars@gmail.com>
"""


import datetime  # Basic date and time types
from random import choice  # Generate pseudo-random numbers
try:
    import thread  # Low-level threading API (Python 2.7)
except ImportError:
    import _thread as thread  # Low-level threading API (Python 3.x)

from dragonfire.reminder import Reminder
import spacy  # Industrial-strength Natural Language Processing in Python

nlp = spacy.load('en')  # Load en_core_web_sm, English, 50 MB, default model
reminder = Reminder()


class IsReminder():
    """Class to contains checking note part of taking notes process with simply if-else struct.
    """

    def compare1(self, h, doc, note_taker, user_answering_note, userin, user_prefix):
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

    def compare2(self, com, h, doc, note_taker, user_answering_note, userin, user_prefix):
        """Method to dragonfire's second command struct for checking reminder of taking note ability.

        Args:
            h:                          doc's helper.
            doc:                        object with nlp from user answering to doc.
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
                    user_answering_note['status'] = False
                    user_answering_note['isRemind'] = False
                    user_answering_note['note_keeper'] = None
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
                                    note_taker.db_upsert(user_answering_note['note_keeper'], None, time, None, None, False, True, True)
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
                                    note_taker.db_upsert(user_answering_note['note_keeper'], None, time, None, None, False, True, True)
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
                                    note_taker.db_upsert(user_answering_note['note_keeper'], None, time, None, None, False, True, True)
                                    # return userin.say(str(time))
                                else:
                                    return userin.say("Repeat!")
                    user_answering_note['status'] = False
                    user_answering_note['isRemind'] = False
                    user_answering_note['note_keeper'] = None
                    if not user_answering_note['is_active']:  # if reminder checker loop not run, start the loop.
                        thread.start_new_thread(reminder.reminde, (note_taker, userin, user_prefix, user_answering_note))
                    return userin.say(choice(["It's okay", "Get it", "note was recorded", "The note taken"]) + choice(
                        [", " + user_prefix + ". ", ". "]) + choice(
                        ["Reminder Added.", "I'm waiting to remind.", "I will remind.",
                         "Reminder has been set."]))
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
