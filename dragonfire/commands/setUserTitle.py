#!/usr/bin/python3
# -*- coding: utf-8 -*-

"""
.. module:: setUseerTitle
    :platform: Unix
    :synopsis: the top-level submodule of Dragonfire.commands that contains the classes related to Dragonfire's simple if-else struct of setting
    user title ability.

.. moduleauthors:: Mehmet Mert Yıldıran <mert.yildiran@bil.omu.edu.tr>
                   Cem Baybars GÜÇLÜ <cem.baybars@gmail.com>
"""

import spacy  # Industrial-strength Natural Language Processing in Python
from tinydb import Query, TinyDB  # TinyDB is a lightweight document oriented database optimized for your happiness

from dragonfire.nlplib import Classifier, Helper  # Submodule of Dragonfire to handle extra NLP tasks

nlp = spacy.load('en')  # Load en_core_web_sm, English, 50 MB, default model


class SetUserTitleCommands():
    """Class to contains user title setting commands with simply if-else struct.
    """

    def compare(self, com, args, userin, config_file, user_prefix):
        """Method to dragonfire's command structures of setting user title ability.

        Args:
            com (str):                 User's command.
            userin:                    :class:`dragonfire.utilities.TextToAction` instance.
            args:                      Command-line arguments.
            config_file:               virtual assistant config file
        """

        doc = nlp(com)
        h = Helper(doc)
        if h.check_lemma("be") and h.check_lemma("-PRON-") and (
                h.check_lemma("lady") or h.check_lemma("woman") or h.check_lemma("girl")):
            config_file.update({'gender': 'female'}, Query().datatype == 'gender')
            config_file.remove(Query().datatype == 'callme')
            user_prefix = "my lady"
            return userin.say("Pardon, " + user_prefix + ".")
        if h.check_lemma("be") and h.check_lemma("-PRON-") and (
                h.check_lemma("sir") or h.check_lemma("man") or h.check_lemma("boy")):
            config_file.update({'gender': 'male'}, Query().datatype == 'gender')
            config_file.remove(Query().datatype == 'callme')
            user_prefix = "sir"
            return userin.say("Pardon, " + user_prefix + ".")
        if h.check_lemma("call") and h.check_lemma("-PRON-"):
            title = ""
            for token in doc:
                if token.pos_ == "NOUN":
                    title += ' ' + token.text
            title = title.strip()
            if not args["server"]:
                callme_config = config_file.search(Query().datatype == 'callme')
                if callme_config:
                    config_file.update({'title': title}, Query().datatype == 'callme')
                else:
                    config_file.insert({'datatype': 'callme', 'title': title})
            user_prefix = title
            return userin.say("OK, " + user_prefix + ".")
        return None
