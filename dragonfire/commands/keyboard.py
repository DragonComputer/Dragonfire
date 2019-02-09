#!/usr/bin/python3
# -*- coding: utf-8 -*-

"""
.. module:: keyboard
    :platform: Unix
    :synopsis: the top-level submodule of Dragonfire.commands that contains the classes related to Dragonfire's simple if-else struct of Keyboard keys ability.

.. moduleauthors:: Mehmet Mert Yıldıran <mert.yildiran@bil.omu.edu.tr>
                   Cem Baybars GÜÇLÜ <cem.baybars@gmail.com>
"""

from pykeyboard import PyKeyboard  # A simple, cross-platform Python module for providing keyboard control
from pymouse import PyMouse  # Cross-platform Python mouse module
from os.path import expanduser  # Common pathname manipulations
from tinydb import TinyDB  # TinyDB is a lightweight document oriented database optimized for your happiness

from dragonfire.utilities import nostdout, nostderr  # Submodule of Dragonfire to provide various utilities


class KeyboardCommands():
    """Class to contains keyboard commands with simply if-else struct.
    """

    def __init__(self, testing=False):
        """Initialization method of :class:`dragonfire.commands.KeyboardCommands` class.
        """

        self.testing = testing
        if self.testing:
            home = expanduser("~")
            self.config_file = TinyDB(home + '/.dragonfire_config.json')

    def compare(self, com, doc, h, args, testing):
        """Method to dragonfire's command structures of keyboard keys ability.

        Args:
            com (str):                 User's command.
            doc:                       doc of com from __init__.py
            h:                         doc helper from __init__.py
            args:                      Command-line arguments.
            testing:                   testing form __init__.py
        """

        self.testing = testing

        if (h.check_nth_lemma(0, "keyboard") or h.check_nth_lemma(0, "type")) and not args["server"]:
            n = len(doc[0].text) + 1
            with nostdout():
                with nostderr():
                    k = PyKeyboard()
                    if not self.testing:
                        for character in com[n:]:
                            k.tap_key(character)
                        k.tap_key(" ")
            return "keyboard"
        if (h.directly_equal(["enter"]) or (h.check_adj_lemma("new") and h.check_noun_lemma("line"))) and not args["server"]:
            with nostdout():
                with nostderr():
                    k = PyKeyboard()
                    if not self.testing:
                        k.tap_key(k.enter_key)
            return "enter"
        if h.check_adj_lemma("new") and h.check_noun_lemma("tab") and not args["server"]:
            with nostdout():
                with nostderr():
                    k = PyKeyboard()
                    if not self.testing:
                        k.press_keys([k.control_l_key, 't'])
            return "new tab"
        if h.check_verb_lemma("switch") and h.check_noun_lemma("tab") and not args["server"]:
            with nostdout():
                with nostderr():
                    k = PyKeyboard()
                    if not self.testing:
                        k.press_keys([k.control_l_key, k.tab_key])
            return "switch tab"
        if h.directly_equal(["CLOSE", "ESCAPE"]) and not args["server"]:
            with nostdout():
                with nostderr():
                    k = PyKeyboard()
                    if not self.testing:
                        k.press_keys([k.control_l_key, 'w'])
                        k.tap_key(k.escape_key)
            return "close"
        if h.check_lemma("back") and h.max_word_count(4) and not args["server"]:
            with nostdout():
                with nostderr():
                    k = PyKeyboard()
                    if not self.testing:
                        k.press_keys([k.alt_l_key, k.left_key])
            return "back"
        if h.check_lemma("forward") and h.max_word_count(4) and not args["server"]:
            with nostdout():
                with nostderr():
                    k = PyKeyboard()
                    if not self.testing:
                        k.press_keys([k.alt_l_key, k.right_key])
            return "forward"
        if (h.check_text("swipe") or h.check_text("scroll")) and not args["server"]:
            if h.check_text("left"):
                with nostdout():
                    with nostderr():
                        m = PyMouse()
                        if not self.testing:
                            m.scroll(0, -5)
                return "swipe left"
            if h.check_text("right"):
                with nostdout():
                    with nostderr():
                        m = PyMouse()
                        if not self.testing:
                            m.scroll(0, 5)
                return "swipe right"
            if h.check_text("up"):
                with nostdout():
                    with nostderr():
                        m = PyMouse()
                        if not self.testing:
                            m.scroll(5, 0)
                return "swipe up"
            if h.check_text("down"):
                with nostdout():
                    with nostderr():
                        m = PyMouse()
                        if not self.testing:
                            m.scroll(-5, 0)
                return "swipe down"
        if h.directly_equal(["PLAY", "PAUSE", "SPACEBAR"]) and not args["server"]:
            with nostdout():
                with nostderr():
                    k = PyKeyboard()
                    if not self.testing:
                        k.tap_key(" ")
            return "play"
        return None
