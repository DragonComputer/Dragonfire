#!/usr/bin/python3
# -*- coding: utf-8 -*-

"""
.. module:: finddInWikipedia
    :platform: Unix
    :synopsis: the top-level submodule of Dragonfire.commands that contains the classes related to Dragonfire's simple if-else struct of searching in wikipedia ability.

.. moduleauthors:: Mehmet Mert Yıldıran <mert.yildiran@bil.omu.edu.tr>
                   Cem Baybars GÜÇLÜ <cem.baybars@gmail.com>
"""

import re  # Regular expression operations

from dragonfire.nlplib import Classifier, Helper  # Submodule of Dragonfire to handle extra NLP tasks
from dragonfire.utilities import TextToAction, nostdout, \
    nostderr  # Submodule of Dragonfire to provide various utilities

import spacy  # Industrial-strength Natural Language Processing in Python
import wikipedia  # Python library that makes it easy to access and parse data from Wikipedia
import wikipedia.exceptions  # Exceptions of wikipedia library
import requests.exceptions  # HTTP for Humans

nlp = spacy.load('en')  # Load en_core_web_sm, English, 50 MB, default model


class FindInWikiCommand():
    """Class to contains taking notes process with simply if-else struct.
    """

    def first_compare(self, com, USER_ANSWERING_WIKI, userin, user_prefix):
        """Method to dragonfire's first command struct of searching in wikipedia ability.

        Args:
            com (str):                 User's command.
            USER_ANSWERING_WIKI:       User answering string array.
            userin:                    :class:`dragonfire.utilities.TextToAction` instance.
            user_prefix:               user's preferred titles.
        """

        doc = nlp(com)
        h = Helper(doc)
        if (h.check_lemma("search") or h.check_lemma("find")) and h.check_lemma("wikipedia"):
            with nostderr():
                search_query = ""
                for token in doc:
                    if not (
                            token.lemma_ == "search" or token.lemma_ == "find" or token.lemma_ == "wikipedia" or token.is_stop):
                        search_query += ' ' + token.text
                search_query = search_query.strip()
                if search_query:
                    try:
                        wikiresult = wikipedia.search(search_query)
                        if len(wikiresult) == 0:
                            userin.say(
                                "Sorry, " + user_prefix + ". But I couldn't find anything about " + search_query + " in Wikipedia.")
                            return True
                        wikipage = wikipedia.page(wikiresult[0])
                        wikicontent = "".join([i if ord(i) < 128 else ' ' for i in wikipage.content])
                        wikicontent = re.sub(r'\([^)]*\)', '', wikicontent)
                        userin.execute(["sensible-browser", wikipage.url], search_query)
                        return userin.say(wikicontent, cmd=["sensible-browser", wikipage.url])
                    except requests.exceptions.ConnectionError:
                        userin.execute([" "], "Wikipedia connection error.")
                        return userin.say("Sorry, " + user_prefix + ". But I'm unable to connect to Wikipedia servers.")
                    except wikipedia.exceptions.DisambiguationError as disambiguation:
                        USER_ANSWERING_WIKI['status'] = True
                        USER_ANSWERING_WIKI['for'] = 'wikipedia'
                        USER_ANSWERING_WIKI['reason'] = 'disambiguation'
                        USER_ANSWERING_WIKI['options'] = disambiguation.options[:3]
                        notify = "Wikipedia disambiguation. Which one of these you meant?:\n - " + \
                                 disambiguation.options[0]
                        msg = user_prefix + ", there is a disambiguation. Which one of these you meant? " + \
                              disambiguation.options[0]
                        for option in disambiguation.options[1:3]:
                            msg += ", or " + option
                            notify += "\n - " + option
                        notify += '\nSay, for example: "THE FIRST ONE" to choose.'
                        userin.execute([" "], notify)
                        return userin.say(msg)
                    except BaseException:
                        pass

    def second_compare(self, com, USER_ANSWERING_WIKI, userin, user_prefix):
        """Method to dragonfire's first command struct of searching in wikipedia ability.

        Args:
            com (str):                 User's command.
            USER_ANSWERING_WIKI:       User answering string array.
            userin:                    :class:`dragonfire.utilities.TextToAction` instance.
            user_prefix:               user's preferred titles.
        """

        if USER_ANSWERING_WIKI['status']:
            if com.startswith("FIRST") or com.startswith("THE FIRST") or com.startswith("SECOND") or com.startswith(
                    "THE SECOND") or com.startswith("THIRD") or com.startswith("THE THIRD"):
                USER_ANSWERING_WIKI['status'] = False
                selection = None
                if com.startswith("FIRST") or com.startswith("THE FIRST"):
                    selection = 0
                elif com.startswith("SECOND") or com.startswith("THE SECOND"):
                    selection = 1
                elif com.startswith("THIRD") or com.startswith("THE THIRD"):
                    selection = 2

                if USER_ANSWERING_WIKI['for'] == 'wikipedia':
                    with nostderr():
                        search_query = USER_ANSWERING_WIKI['options'][selection]
                        try:
                            wikiresult = wikipedia.search(search_query)
                            if len(wikiresult) == 0:
                                userin.say(
                                    "Sorry, " + user_prefix + ". But I couldn't find anything about " + search_query + " in Wikipedia.")
                                return True
                            wikipage = wikipedia.page(wikiresult[0])
                            wikicontent = "".join([i if ord(i) < 128 else ' ' for i in wikipage.content])
                            wikicontent = re.sub(r'\([^)]*\)', '', wikicontent)
                            userin.execute(["sensible-browser", wikipage.url], search_query)
                            return userin.say(wikicontent, cmd=["sensible-browser", wikipage.url])
                        except requests.exceptions.ConnectionError:
                            userin.execute([" "], "Wikipedia connection error.")
                            return userin.say(
                                "Sorry, " + user_prefix + ". But I'm unable to connect to Wikipedia servers.")
                        except Exception:
                            return False
