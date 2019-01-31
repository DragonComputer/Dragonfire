#!/usr/bin/python3
# -*- coding: utf-8 -*-

"""
.. module:: findInYoutube
    :platform: Unix
    :synopsis: the top-level submodule of Dragonfire.commands that contains the classes related to Dragonfire's simple if-else struct of Searching in Youtube ability.

.. moduleauthors:: Mehmet Mert Yıldıran <mert.yildiran@bil.omu.edu.tr>
                   Cem Baybars GÜÇLÜ <cem.baybars@gmail.com>
"""
import time

import youtube_dl # Command-line program to download videos from YouTube.com and other video sites
from pykeyboard import PyKeyboard # A simple, cross-platform Python module for providing keyboard control
import spacy  # Industrial-strength Natural Language Processing in Python

from dragonfire.utilities import TextToAction, nostdout, nostderr  # Submodule of Dragonfire to provide various utilities
from dragonfire.nlplib import Classifier, Helper  # Submodule of Dragonfire to handle extra NLP tasks

nlp = spacy.load('en')  # Load en_core_web_sm, English, 50 MB, default model


class FindInYoutubeCommand():
    """Class to contains youtube video finder with simply if-else struct.
    """

    def compare(self, com, args, userin, user_prefix):
        """Method to dragonfire's command structures of searching in youtube ability.

        Args:
            com (str):                 User's command.
            userin:                    :class:`dragonfire.utilities.TextToAction` instance.
            args:                      Command-line arguments.

        Keyword Args:
            user_prefix:               user's preferred titles.
        """

        doc = nlp(com)
        h = Helper(doc)
        if (h.check_lemma("search") or h.check_lemma("find")) and h.check_lemma("youtube"):
            with nostdout():
                with nostderr():
                    search_query = ""
                    for token in doc:
                        if not (
                                token.lemma_ == "search" or token.lemma_ == "find" or token.lemma_ == "youtube" or token.is_stop):
                            search_query += ' ' + token.text
                    search_query = search_query.strip()
                    if search_query:
                        info = youtube_dl.YoutubeDL({}).extract_info('ytsearch:' + search_query, download=False,
                                                                     ie_key='YoutubeSearch')
                        if len(info['entries']) > 0:
                            youtube_title = info['entries'][0]['title']
                            youtube_url = "https://www.youtube.com/watch?v=%s" % (info['entries'][0]['id'])
                            userin.execute(["sensible-browser", youtube_url], youtube_title)
                            youtube_title = "".join([i if ord(i) < 128 else ' ' for i in youtube_title])
                            response = userin.say(youtube_title, ["sensible-browser", youtube_url])
                        else:
                            youtube_title = "No video found, " + user_prefix + "."
                            response = userin.say(youtube_title)
                        k = PyKeyboard()
                        if not args["server"] and not self.testing:
                            time.sleep(5)
                            k.tap_key(k.tab_key)
                            k.tap_key(k.tab_key)
                            k.tap_key(k.tab_key)
                            k.tap_key(k.tab_key)
                            k.tap_key('f')
                        return response
        return None
