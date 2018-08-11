#!/usr/bin/python3
# -*- coding: utf-8 -*-

"""
.. module:: utilities
    :platform: Unix
    :synopsis: the top-level submodule of Dragonfire that provides various utility tools for different kind of tasks.

.. moduleauthor:: Mehmet Mert Yıldıran <mert.yildiran@bil.omu.edu.tr>
"""

import inspect  # Inspect live objects
import os  # Miscellaneous operating system interfaces
import subprocess  # Subprocess managements
import time  # Time access and conversions
from multiprocessing import Pool  # Process-based “threading” interface
from sys import stdout  # System-specific parameters and functions
from random import randint  # Generate pseudo-random numbers
import contextlib  # Utilities for with-statement contexts
try:
    import cStringIO  # Read and write strings as files (Python 2.7)
except ImportError:
    import io as cStringIO  # Read and write strings as files (Python 3.x)
import sys  # System-specific parameters and functions

import realhud  # Dragonfire's Python C extension to display a click-through, transparent background images or GIFs

from tweepy.error import TweepError  # An easy-to-use Python library for accessing the Twitter API
import metadata_parser  # Python library for pulling metadata out of web documents
import urllib.request  # URL handling modules
import mimetypes  # Map filenames to MIME types
import uuid  # UUID objects according to RFC 4122
import shutil  # High-level file operations

DRAGONFIRE_PATH = os.path.dirname(os.path.abspath(inspect.getfile(inspect.currentframe())))
FNULL = open(os.devnull, 'w')
TWITTER_CHAR_LIMIT = 280

songRunning = False


class TextToAction:
    """Class that turns text into action.
    """

    def __init__(self, args, testing=False):
        """Initialization method of :class:`dragonfire.utilities.TextToAction` class.

        Args:
            args:  Command-line arguments.
        """

        self.headless = args["headless"]
        self.silent = args["silent"]
        self.server = args["server"]
        self.testing = testing
        if self.server:
            self.headless = True
            self.silent = True
        self.twitter_api = None
        self.twitter_user = None
        if not self.headless:
            realhud.load_gif(DRAGONFIRE_PATH + "/realhud/animation/avatar.gif")

    def execute(self, cmd="", msg="", speak=False, duration=0):
        """Method to execute the given bash command and display a desktop environment independent notification.

        Keyword Args:
            cmd (str):          Bash command.
            msg (str):          Message to be displayed.
            speak (bool):       Also call the :func:`dragonfire.utilities.TextToAction.say` method with this message?
            duration (int):     Wait n seconds before executing the bash command.

        .. note::

            Because this method is executing bash commands directly, it should be called and modified **carefully**. Otherwise it can cause a **SECURITY BREACH** on the machine.

        """

        self.speak = speak

        if self.server or not self.testing:
            if self.speak:
                self.say(msg)
            try:
                subprocess.Popen(["notify-send", "Dragonfire", msg])
            except BaseException:
                pass
            if cmd != "":
                time.sleep(duration)
                try:
                    subprocess.Popen(cmd, stdout=FNULL, stderr=FNULL)
                except BaseException:
                    pass
        return msg

    def say(self, msg, dynamic=False, end=False, cmd=None):
        """Method to give text-to-speech output(using **The Festival Speech Synthesis System**), print the response into console and **send a tweet**.

        Args:
            msg (str):  Message to be read by Dragonfire or turned into a tweet.

        Keyword Args:
            dynamic (bool):     Dynamically print the output into console?
            end (bool):         Is it the end of the dynamic printing?
            cmd (str):          Bash command.

        Returns:
            bool:  True or False

        .. note::

            This method is extremely polymorphic so use it carefully.
             - If you call it on `--server` mode it tweets. Otherwise it prints the reponse into console.
             - If `--silent` option is not fed then it also gives text-to-speech output. Otherwise it remain silent.
             - If response is more than 10000 characters it does not print.
             - If `--headless` option is not fed then it shows a speaking female head animation on the screen using `realhud` Python C extension.

        """

        if self.server:
            text = "@" + self.twitter_user + " " + msg  # .upper()
            text = (text[:TWITTER_CHAR_LIMIT]) if len(text) > TWITTER_CHAR_LIMIT else text
            if cmd:
                if len(cmd) > 1:
                    if cmd[0] == "sensible-browser":
                        reduction = len(text + " " + cmd[1]) - TWITTER_CHAR_LIMIT
                        if reduction < 1:
                            reduction = None
                        text = text[:reduction] + " " + cmd[1]
                        page = metadata_parser.MetadataParser(url=cmd[1])
                        img_url = page.get_metadata_link('image')
                        if img_url:
                            response = urllib.request.urlopen(img_url)
                            img_data = response.read()
                            img_extension = mimetypes.guess_extension(response.headers['content-type'])
                            filename = "/tmp/tmp" + uuid.uuid4().hex + img_extension
                            with open(filename, 'wb') as f:
                                f.write(img_data)

                            try:
                                self.twitter_api.update_with_media(filename, text)
                                if randint(1, 3) == 1:
                                    self.twitter_api.create_friendship(self.twitter_user, follow=True)
                            except TweepError as e:
                                print("Warning: " + e.response.text)
                            finally:
                                os.remove(filename)
                            return msg
            try:
                self.twitter_api.update_status(text)
                if randint(1, 10) == 1:
                    self.twitter_api.create_friendship(self.twitter_user, follow=True)
            except TweepError as e:
                print("Warning: " + e.response.text)
            return msg
        # if songRunning == True:
        #   subprocess.Popen(["rhythmbox-client","--pause"])
        if len(msg) < 10000:
            (columns, lines) = shutil.get_terminal_size()
            if dynamic:
                if end:
                    print(msg.upper())
                    print(columns * "_" + "\n")
                else:
                    print("Dragonfire: " + msg.upper(), end=' ')
                    stdout.flush()
            else:
                print("Dragonfire: " + msg.upper())
                print(columns * "_" + "\n")
        if not self.silent:
            subprocess.call(["pkill", "flite"], stdout=FNULL, stderr=FNULL)
            tts_proc = subprocess.Popen(
                "flite -voice slt -f /dev/stdin",
                stdin=subprocess.PIPE,
                stdout=FNULL,
                stderr=FNULL,
                shell=True)
            msg = "".join([i if ord(i) < 128 else ' ' for i in msg])
            tts_proc.stdin.write(msg.encode())
            tts_proc.stdin.close()
            # print "TTS process started."

        pool = Pool(processes=1)
        if not self.headless:
            pool.apply_async(realhud.play_gif, [0.5, True])
            # print "Avatar process started."

        if not self.silent:
            tts_proc.wait()
        pool.terminate()
        # if songRunning == True:
        #   subprocess.Popen(["rhythmbox-client","--play"])
        return msg

    def espeak(self, msg):
        """Method to give a text-to-speech output using **eSpeak: Speech Synthesizer**.

        Args:
            msg (str):  Message to be read by Dragonfire.

        .. note::

            This method is currently not used by Dragonfire and deprecated.

        """

        subprocess.Popen(["espeak", "-v", "en-uk-north", msg])

    def pretty_print_nlp_parsing_results(self, doc):
        """Method to print the nlp parsing results in a pretty way.

        Args:
            doc:  A :class:`Doc` instance from :mod:`spacy` library.

        .. note::

            This method is only called when `--verbose` option fed.

        """

        if len(doc) > 0:
            print("")
            print("{:12}  {:12}  {:12}  {:12} {:12}  {:12}  {:12}  {:12}".format("TEXT", "LEMMA", "POS", "TAG", "DEP", "SHAPE", "ALPHA", "STOP"))
            for token in doc:
                print("{:12}  {:12}  {:12}  {:12} {:12}  {:12}  {:12}  {:12}".format(token.text, token.lemma_, token.pos_, token.tag_, token.dep_, token.shape_, str(token.is_alpha), str(token.is_stop)))
            print("")
        if len(list(doc.noun_chunks)) > 0:
            print("{:12}  {:12}  {:12}  {:12}".format("TEXT", "ROOT.TEXT", "ROOT.DEP_", "ROOT.HEAD.TEXT"))
            for chunk in doc.noun_chunks:
                print("{:12}  {:12}  {:12}  {:12}".format(chunk.text, chunk.root.text, chunk.root.dep_, chunk.root.head.text))
            print("")


@contextlib.contextmanager
def nostdout():
    """Method to suppress the standard output. (use it with `with` statements)
    """

    save_stdout = sys.stdout
    sys.stdout = cStringIO.StringIO()
    yield
    sys.stdout = save_stdout


@contextlib.contextmanager
def nostderr():
    """Method to suppress the standard error. (use it with `with` statements)
    """
    save_stderr = sys.stderr
    sys.stderr = cStringIO.StringIO()
    yield
    sys.stderr = save_stderr


def omniscient_coefficient_optimizer():
    from dragonfire.omniscient import Omniscient
    import spacy

    dataset = [
        ("Where is the Times Square", ["New York City"]),
        ("What is the height of Burj Khalifa", ["828 m"]),
        ("Where is Burj Khalifa", ["Dubai"]),
        ("What is the height of Great Pyramid of Giza", ["480.6 ft"]),
        ("Who is playing Jon Snow in Game of Thrones", ["Kit Harington"]),
        ("What is the atomic number of oxygen", ["8"]),
        ("What is the official language of Japan", ["Japanese"]),
        ("What is the real name of Iron Man", ["Tony", "Stark", "Tony Stark"]),
        ("Who is the conqueror of Constantinople", ["Mehmed II", "Mehmet II", "Mehmet"]),
        ("When Constantinople was conquered", ["1453"]),
        ("What is the capital of Turkey", ["Ankara"]),
        ("What is the largest city of Turkey", ["Istanbul"]),
        ("What is the name of the world's best university", ["Harvard", "Peking University"]),
        ("What is the name of the world's longest river", ["Nile", "Amazon"]),
        ("What is the brand of the world's most expensive car", ["Rolls-Royce"]),
        ("What is the bloodiest war in human history", ["World War II", "World War I"]),
        ("What is the name of the best seller book", ["Real Marriage", "'Real Marriage' on"]),
        ("What is the lowest point in the ocean", ["the Mariana Trench"]),
        ("Who invented General Relativity", ["Einstein"]),
        ("When was United Nations formed", ["1945"])
    ]

    omniscient = Omniscient(spacy.load('en'))
    best_score = 0
    best_coefficient = None
    i = 0
    while True:
        i += 1
        print("Iteration: " + str(i))
        score = 0
        omniscient.randomize_coefficients()
        print(omniscient.coefficient)

        for (question, answers) in dataset:
            if omniscient.respond(question) in answers: score += 1

        # purpose of this block is finding the optimum value for coefficients
        if score > best_score:
            print("\n--- !!! NEW BEST !!! ---")
            best_score = score
            best_coefficient = omniscient.coefficient
            print(str(best_score) + ' / ' + len(dataset))
            print(best_coefficient)
            print("------------------------\n")
