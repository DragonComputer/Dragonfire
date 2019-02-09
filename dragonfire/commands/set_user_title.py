#!/usr/bin/python3
# -*- coding: utf-8 -*-

"""
.. module:: set_user_title
    :platform: Unix
    :synopsis: the top-level submodule of Dragonfire.commands that contains the classes related to Dragonfire's simple if-else struct of setting
    user title ability.

.. moduleauthors:: Mehmet Mert Yıldıran <mert.yildiran@bil.omu.edu.tr>
                   Cem Baybars GÜÇLÜ <cem.baybars@gmail.com>
"""

from tinydb import Query  # TinyDB is a lightweight document oriented database optimized for your happiness


class SetUserTitleCommands():
    """Class to contains user title setting commands with simply if-else struct.
    """

    def compare(self, doc, h, args, userin, config_file):
        """Method to dragonfire's command structures of setting user title ability.

        Args:
            doc:                       doc of com from __init__.py
            h:                         doc helper from __init__.py
            userin:                    :class:`dragonfire.utilities.TextToAction` instance.
            args:                      Command-line arguments.
            config_file:               virtual assistant config file
        """

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
