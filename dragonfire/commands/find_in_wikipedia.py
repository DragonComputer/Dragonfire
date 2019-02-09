#!/usr/bin/python3
# -*- coding: utf-8 -*-

"""
.. module:: find_in_wikipedia
    :platform: Unix
    :synopsis: the top-level submodule of Dragonfire.commands that contains the classes related to Dragonfire's simple if-else struct of searching in wikipedia ability.

.. moduleauthors:: Mehmet Mert Yıldıran <mert.yildiran@bil.omu.edu.tr>
                   Cem Baybars GÜÇLÜ <cem.baybars@gmail.com>
"""

import re  # Regular expression operations
import wikipedia  # Python library that makes it easy to access and parse data from Wikipedia
import wikipedia.exceptions  # Exceptions of wikipedia library
import requests.exceptions  # HTTP for Humans

from dragonfire.utilities import nostderr  # Submodule of Dragonfire to provide various utilities


class FindInWikiCommand():
    """Class to contains searching in wikipedia process with simply if-else struct.
    """

    def first_compare(self, doc, h, user_answering_wiki, userin, user_prefix):
        """Method to dragonfire's first command struct of searching in wikipedia ability.

        Args:
            doc:                       doc of com from __init__.py
            h:                         doc helper from __init__.py
            user_answering_wiki:       User answering string array.
            userin:                    :class:`dragonfire.utilities.TextToAction` instance.
            user_prefix:               user's preferred titles.
        """

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
                        user_answering_wiki['status'] = True
                        user_answering_wiki['for'] = 'wikipedia'
                        user_answering_wiki['reason'] = 'disambiguation'
                        user_answering_wiki['options'] = disambiguation.options[:3]
                        notify = "Wikipedia disambiguation. Which one of these you meant?:\n - " + disambiguation.options[0]
                        msg = user_prefix + ", there is a disambiguation. Which one of these you meant? " + disambiguation.options[0]
                        for option in disambiguation.options[1:3]:
                            msg += ", or " + option
                            notify += "\n - " + option
                        notify += '\nSay, for example: "THE FIRST ONE" to choose.'
                        userin.execute([" "], notify)
                        return userin.say(msg)
                    except BaseException:
                        pass
        return None

    def second_compare(self, com, user_answering_wiki, userin, user_prefix):
        """Method to dragonfire's first command struct of searching in wikipedia ability.

        Args:
            com (str):                 User's command.
            user_answering_wiki:       User answering string array.
            userin:                    :class:`dragonfire.utilities.TextToAction` instance.
            user_prefix:               user's preferred titles.
        """

        if user_answering_wiki['status']:
            if com.startswith("FIRST") or com.startswith("THE FIRST") or com.startswith("SECOND") or com.startswith(
                    "THE SECOND") or com.startswith("THIRD") or com.startswith("THE THIRD"):
                user_answering_wiki['status'] = False
                selection = None
                if com.startswith("FIRST") or com.startswith("THE FIRST"):
                    selection = 0
                elif com.startswith("SECOND") or com.startswith("THE SECOND"):
                    selection = 1
                elif com.startswith("THIRD") or com.startswith("THE THIRD"):
                    selection = 2

                if user_answering_wiki['for'] == 'wikipedia':
                    with nostderr():
                        search_query = user_answering_wiki['options'][selection]
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
        return None
