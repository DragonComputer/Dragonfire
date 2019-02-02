#!/usr/bin/python3
# -*- coding: utf-8 -*-

"""
.. module:: find_in_browser
    :platform: Unix
    :synopsis: the top-level submodule of Dragonfire.commands that contains the classes related to Dragonfire's simple if-else struct of Searching on Browser ability.

.. moduleauthors:: Mehmet Mert Yıldıran <mert.yildiran@bil.omu.edu.tr>
                   Cem Baybars GÜÇLÜ <cem.baybars@gmail.com>
"""

import spacy  # Industrial-strength Natural Language Processing in Python

from dragonfire.utilities import TextToAction, nostdout, nostderr  # Submodule of Dragonfire to provide various utilities
from dragonfire.nlplib import Classifier, Helper  # Submodule of Dragonfire to handle extra NLP tasks

nlp = spacy.load('en')  # Load en_core_web_sm, English, 50 MB, default model


class FindInBrowserCommand():
    """Class to contains browser content finder with simply if-else struct.
    """

    def compare_content(self, com, userin, user_prefix):
        """Method to dragonfire's command structures of Searching on Browser ability.

        Args:
            com (str):                 User's command.
            userin:                    :class:`dragonfire.utilities.TextToAction` instance.

        Keyword Args:
            user_prefix:               user's preferred titles.
        """

        doc = nlp(com)
        h = Helper(doc)
        if (h.check_lemma("search") or h.check_lemma("find")) and (
                h.check_lemma("google") or h.check_lemma("web") or h.check_lemma("internet")) and not h.check_lemma(
                "image"):
            with nostdout():
                with nostderr():
                    search_query = ""
                    for token in doc:
                        if not (
                                token.lemma_ == "search" or token.lemma_ == "find" or token.lemma_ == "google" or token.lemma_ == "web" or token.lemma_ == "internet" or token.is_stop):
                            search_query += ' ' + token.text
                    search_query = search_query.strip()
                    if search_query:
                        tab_url = "http://google.com/?#q=" + search_query
                        return userin.execute(["sensible-browser", tab_url], search_query, True)
        return None

    def compare_image(self, com, userin, user_prefix):
        """Method to dragonfire's command structures of Searching on Browser ability.

        Args:
            com (str):                 User's command.
            userin:                    :class:`dragonfire.utilities.TextToAction` instance.

        Keyword Args:
            user_prefix:               user's preferred titles.
        """

        doc = nlp(com)
        h = Helper(doc)
        if (h.check_lemma("search") or h.check_lemma("find")) and (
                h.check_lemma("google") or h.check_lemma("web") or h.check_lemma("internet")) and h.check_lemma(
                "image"):
            with nostdout():
                with nostderr():
                    search_query = ""
                    for token in doc:
                        if not (
                                token.lemma_ == "search" or token.lemma_ == "find" or token.lemma_ == "google" or token.lemma_ == "web" or token.lemma_ == "internet" or token.lemma_ == "image" or token.is_stop):
                            search_query += ' ' + token.text
                    search_query = search_query.strip()
                    if search_query:
                        tab_url = "http://google.com/?#q=" + search_query + "&tbm=isch"
                        return userin.execute(["sensible-browser", tab_url], search_query, True)
        return None
