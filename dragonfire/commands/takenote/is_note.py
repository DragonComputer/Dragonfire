#!/usr/bin/python3
# -*- coding: utf-8 -*-

"""
.. module:: is_note
    :platform: Unix
    :synopsis: the top-level submodule of Dragonfire.commands.takenote that contains the class related to Dragonfire's simple if-else struct of create note of taking note ability.

.. moduleauthor:: Cem Baybars GÜÇLÜ <cem.baybars@gmail.com>
"""

from random import choice  # Generate pseudo-random numbers

import spacy  # Industrial-strength Natural Language Processing in Python

nlp = spacy.load('en')  # Load en_core_web_sm, English, 50 MB, default model


class IsNote():
    """Class to contains checking note part of taking notes process with simply if-else struct.
    """

    def compare(self, h, doc, note_taker, user_answering_note, userin, user_prefix):
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
