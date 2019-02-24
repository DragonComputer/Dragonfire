#!/usr/bin/python3
# -*- coding: utf-8 -*-

"""
.. module:: __init__
    :platform: Unix
    :synopsis: the top-level module of Dragonfire that contains the entry point and handles built-in commands.

.. moduleauthor:: Mehmet Mert Yıldıran <mert.yildiran@bil.omu.edu.tr>
"""

import argparse  # Parser for command-line options, arguments and sub-commands
import datetime  # Basic date and time types
import inspect  # Inspect live objects
import os  # Miscellaneous operating system interfaces
import re  # Regular expression operations
import subprocess  # Subprocess managements
import sys  # System-specific parameters and functions
try:
    import thread  # Low-level threading API (Python 2.7)
except ImportError:
    import _thread as thread  # Low-level threading API (Python 3.x)
import time  # Time access and conversions
import uuid  # UUID objects according to RFC 4122
from multiprocessing import Event, Process  # Process-based “threading” interface
from os.path import expanduser  # Common pathname manipulations
from random import choice  # Generate pseudo-random numbers
import shutil  # High-level file operations
import readline  # GNU readline interface

from dragonfire.learn import Learner  # Submodule of Dragonfire that forms her learning ability
from dragonfire.nlplib import Classifier, Helper  # Submodule of Dragonfire to handle extra NLP tasks
from dragonfire.omniscient import Omniscient  # Submodule of Dragonfire that serves as a Question Answering Engine
from dragonfire.stray import SystemTrayExitListenerSet, SystemTrayInit  # Submodule of Dragonfire for System Tray Icon related functionalities
from dragonfire.utilities import TextToAction, nostdout, nostderr  # Submodule of Dragonfire to provide various utilities
from dragonfire.arithmetic import arithmetic_parse  # Submodule of Dragonfire to analyze arithmetic expressions
from dragonfire.deepconv import DeepConversation  # Submodule of Dragonfire to answer questions directly using an Artificial Neural Network
from dragonfire.coref import NeuralCoref  # Submodule of Dragonfire that aims to create corefference based dialogs
from dragonfire.config import Config  # Submodule of Dragonfire to store configurations
from dragonfire.database import Base  # Submodule of Dragonfire module that contains the database schema

import spacy  # Industrial-strength Natural Language Processing in Python
import pyowm  # A Python wrapper around the OpenWeatherMap API
import wikipedia  # Python library that makes it easy to access and parse data from Wikipedia
import wikipedia.exceptions  # Exceptions of wikipedia library
import requests.exceptions  # HTTP for Humans
import youtube_dl  # Command-line program to download videos from YouTube.com and other video sites
from pykeyboard import PyKeyboard  # A simple, cross-platform Python module for providing keyboard control
from pymouse import PyMouse  # Cross-platform Python mouse module
from tinydb import Query, TinyDB  # TinyDB is a lightweight document oriented database optimized for your happiness
from sqlalchemy import create_engine  # the Python SQL toolkit and Object Relational Mapper
from sqlalchemy.orm import sessionmaker  # ORM submodule of SQLAlchemy


__version__ = '1.0.0'

DRAGONFIRE_PATH = os.path.dirname(os.path.abspath(inspect.getfile(inspect.currentframe())))
FNULL = open(os.devnull, 'w')
GENDER_PREFIX = {'male': 'sir', 'female': 'my lady'}
CONVERSATION_ID = uuid.uuid4()
userin = None
nlp = spacy.load('en')  # Load en_core_web_sm, English, 50 MB, default model
learner = Learner(nlp)
omniscient = Omniscient(nlp)
dc = DeepConversation()
coref = NeuralCoref()
e = Event()

user_answering = {
    'status': False,
    'for': None,
    'reason': None,
    'options': None
}

try:
    raw_input  # Python 2
except NameError:
    raw_input = input  # Python 3


def start(args, userin):
    """Function that starts the virtual assistant with the correct mode according to command-line arguments.

    Args:
        args:       Command-line arguments.
        userin:     :class:`dragonfire.utilities.TextToAction` instance.
    """

    if 'TRAVIS' in os.environ or args["db"] == "mysql":
        engine = create_engine('mysql+pymysql://' + Config.MYSQL_USER + ':' + Config.MYSQL_PASS + '@' + Config.MYSQL_HOST + '/' + Config.MYSQL_DB)
    else:
        engine = create_engine('sqlite:///dragonfire.db', connect_args={'check_same_thread': False}, echo=True)
    Base.metadata.create_all(engine)
    Base.metadata.bind = engine
    DBSession = sessionmaker(bind=engine)
    db_session = DBSession()
    learner.db_session = db_session

    if args["server"]:
        import dragonfire.api as API  # API of Dragonfire
        import tweepy  # An easy-to-use Python library for accessing the Twitter API
        from tweepy import OAuthHandler
        from tweepy import Stream
        from dragonfire.twitter import MentionListener

        if Config.TWITTER_CONSUMER_KEY != 'CONSUMER_KEY':
            auth = OAuthHandler(Config.TWITTER_CONSUMER_KEY, Config.TWITTER_CONSUMER_SECRET)
            auth.set_access_token(Config.TWITTER_ACCESS_KEY, Config.TWITTER_ACCESS_SECRET)
            userin.twitter_api = tweepy.API(auth)

            print("Listening Twitter mentions...")
            l = MentionListener(args, userin)
            stream = Stream(auth, l)
            stream.filter(track=['DragonfireAI'], async=True)
        API.Run(nlp, learner, omniscient, dc, coref, userin, args["server"], args["port"], db_session)
    else:
        global user_full_name
        global user_prefix
        if args["cli"]:
            her = VirtualAssistant(args, userin, user_full_name, user_prefix)
            while (True):
                com = raw_input("Enter your command: ")
                thread.start_new_thread(her.command, (com,))
                time.sleep(0.5)
        elif args["gspeech"]:
            from dragonfire.sr.gspeech import GspeechRecognizer

            her = VirtualAssistant(args, userin, user_full_name, user_prefix)
            recognizer = GspeechRecognizer()
            recognizer.recognize(her)
        else:
            from dragonfire.sr.deepspeech import DeepSpeechRecognizer

            her = VirtualAssistant(args, userin, user_full_name, user_prefix)
            recognizer = DeepSpeechRecognizer()
            recognizer.recognize(her)


class VirtualAssistant():
    """Class to define a virtual assistant.

    This class provides necessary initiations and a function named :func:`dragonfire.VirtualAssistant.command`
    as the entry point for each one of the user commands.

    .. note::

        This class is not used in the API.

    """

    def __init__(self, args, userin, user_full_name="John Doe", user_prefix="sir", tw_user=None, testing=False):
        """Initialization method of :class:`dragonfire.VirtualAssistant` class.

        Args:
            args:       Command-line arguments.
            userin:     :class:`dragonfire.utilities.TextToAction` instance.

        Keyword Args:
            user_full_name (str):       User's full name  to answer some basic questions
            user_prefix (str):          Prefix to address/call user when answering
            tw_user (str):              Twitter username of the person querying DragonfireAI Twitter account with a mention
        """

        self.args = args
        self.userin = userin
        self.user_full_name = user_full_name
        self.user_prefix = user_prefix
        self.userin.twitter_user = tw_user
        self.testing = testing
        self.inactive = False
        if not self.args["server"]:
            self.inactive = True
        if self.testing:
            home = expanduser("~")
            self.config_file = TinyDB(home + '/.dragonfire_config.json')


    def command(self, com):
        """Function that serves as the entry point for each one of the user commands.

        This function goes through these steps for each one of user's commands, respectively:

         - Search across the built-in commands via a simple if-else control flow.
         - Try to get a response from :func:`dragonfire.arithmetic.arithmetic_parse` function.
         - Try to get a response from :func:`dragonfire.learn.Learner.respond` method.
         - Try to get a answer from :func:`dragonfire.omniscient.Omniscient.respond` method.
         - Try to get a response from :func:`dragonfire.deepconv.DeepConversation.respond` method.

        Args:
            com (str):  User's command.

        Returns:
            str:  Response.
        """

        if not self.args["server"]:
            global config_file
            global e
            if (e.is_set()):  # System Tray Icon exit must trigger this
                exit(0)
        args = self.args
        userin = self.userin
        user_full_name = self.user_full_name
        user_prefix = self.user_prefix
        if self.testing:
            config_file = self.config_file

        if isinstance(com, str) and com:
            com = com.strip()
        else:
            return False

        print("You: " + com.upper())
        doc = nlp(com)
        h = Helper(doc)

        if args["verbose"]:
            userin.pretty_print_nlp_parsing_results(doc)

        # Input: DRAGONFIRE | WAKE UP | HEY
        if self.inactive and not (h.directly_equal(["dragonfire", "hey"]) or (h.check_verb_lemma("wake") and h.check_nth_lemma(-1, "up")) or (h.check_nth_lemma(0, "dragon") and h.check_nth_lemma(1, "fire") and h.max_word_count(2))):
            return ""

        # User is answering to Dragonfire
        if user_answering['status']:
            if com.startswith("FIRST") or com.startswith("THE FIRST") or com.startswith("SECOND") or com.startswith("THE SECOND") or com.startswith("THIRD") or com.startswith("THE THIRD"):
                user_answering['status'] = False
                selection = None
                if com.startswith("FIRST") or com.startswith("THE FIRST"):
                    selection = 0
                elif com.startswith("SECOND") or com.startswith("THE SECOND"):
                    selection = 1
                elif com.startswith("THIRD") or com.startswith("THE THIRD"):
                    selection = 2

                if user_answering['for'] == 'wikipedia':
                    with nostderr():
                        search_query = user_answering['options'][selection]
                        try:
                            wikiresult = wikipedia.search(search_query)
                            if len(wikiresult) == 0:
                                userin.say("Sorry, " + user_prefix + ". But I couldn't find anything about " + search_query + " in Wikipedia.")
                                return True
                            wikipage = wikipedia.page(wikiresult[0])
                            wikicontent = "".join([i if ord(i) < 128 else ' ' for i in wikipage.content])
                            wikicontent = re.sub(r'\([^)]*\)', '', wikicontent)
                            cmds = [{'distro': 'All', 'name': ["sensible-browser", wikipage.url]}]
                            userin.execute(cmds, search_query)
                            return userin.say(wikicontent, cmd=["sensible-browser", wikipage.url])
                        except requests.exceptions.ConnectionError:
                            cmds = [{'distro': 'All', 'name': [" "]}]
                            userin.execute(cmds, "Wikipedia connection error.")
                            return userin.say("Sorry, " + user_prefix + ". But I'm unable to connect to Wikipedia servers.")
                        except Exception:
                            return False

        if user_answering['status'] and user_answering['for'] == 'execute':
            if h.check_text("whatever") or (h.check_text("give") and h.check_text("up")) or (h.check_text("not") and h.check_text("now")) or (h.check_text("forget") and h.check_text("it")):  # for writing interrupt while taking notes and creating reminders.
                user_answering['status'] = False
                return userin.say(
                    choice(["As you wish", "I understand", "Alright", "Ready whenever you want", "Get it"]) + choice([".", ", " + user_prefix + "."]))
            if user_answering['reason'] == 'install':
                user_answering['status'] = False
                if h.check_text("yes") or (h.check_text("do") and h.check_text("it")) or h.check_text("yep") or h.check_text("okay"):
                    cmds = [{'distro': 'All', 'name': ["gksudo", "apt-get install " + user_answering['options'][0]]}]
                    userin.say("Installing " + user_answering['options'][1] + "...")
                    return userin.execute(cmds, "install**" + user_answering['options'][1])
                else:
                    return userin.say("Okay, I won't install!")

        # Input: DRAGONFIRE | WAKE UP | HEY
        if h.directly_equal(["dragonfire", "hey"]) or (h.check_verb_lemma("wake") and h.check_nth_lemma(-1, "up")) or (h.check_nth_lemma(0, "dragon") and h.check_nth_lemma(1, "fire") and h.max_word_count(2)):
            self.inactive = False
            return userin.say(choice([
                "Yes, " + user_prefix + ".",
                "Yes. I'm waiting.",
                "What is your order?",
                "Ready for the orders!",
                user_prefix.capitalize() + ", tell me your wish."
            ]))
        # Input: GO TO SLEEP
        if (h.check_verb_lemma("go") and h.check_noun_lemma("sleep")) or (h.check_verb_lemma("stop") and h.check_verb_lemma("listen")):
            self.inactive = True
            cmds = [{'distro': 'All', 'name': ["echo"]}]
            userin.execute(cmds, "Dragonfire deactivated. To reactivate say 'Dragonfire!' or 'Wake Up!'")
            return userin.say("I'm going to sleep")
        # Input: ENOUGH | SHUT UP
        if h.directly_equal(["enough"]) or (h.check_verb_lemma("shut") and h.check_nth_lemma(-1, "up")):
            tts_kill()
            msg = "Dragonfire quiets."
            print(msg)
            return msg
        # Input: WHAT IS YOUR NAME
        if h.check_wh_lemma("what") and h.check_deps_contains("your name"):
            cmds = [{'distro': 'All', 'name': [" "]}]
            return userin.execute(cmds, "My name is Dragonfire.", True)
        # Input: WHAT IS YOUR GENDER
        if h.check_wh_lemma("what") and h.check_deps_contains("your gender"):
            return userin.say("I have a female voice but I don't have a gender identity. I'm a computer program, " + user_prefix + ".")
        # Input: WHO AM I | SAY MY NAME
        if (h.check_wh_lemma("who") and h.check_text("I")) or (h.check_verb_lemma("say") and h.check_text("my") and h.check_lemma("name")):
            cmds = [{'distro': 'All', 'name': [" "]}]
            userin.execute(cmds, user_full_name)
            return userin.say("Your name is " + user_full_name + ", " + user_prefix + ".")

        # Input OPEN || CLOSE
        if h.check_verb_lemma("open") or h.check_adj_lemma("open") or h.check_verb_lemma("run") or h.check_verb_lemma("start") or h.check_verb_lemma("show") or h.check_verb_lemma("close") or h.check_adj_lemma("close") or h.check_verb_lemma("stop"):
            is_kill = False
            if h.check_verb_lemma("close") or h.check_adj_lemma("close") or h.check_verb_lemma("stop"):  # check for filter to program closing command
                is_kill = True
                # Input: OFFICE SUITE AND WEB BROWSER
            if not is_kill:  # following lines created for differences about opening and closing commands.
                if h.check_noun_lemma("browser") or h.check_text("chrome") or h.check_text("firefox"):
                    cmds = [{'distro': 'All', 'name': ["sensible-browser"]}]
                    return userin.say(userin.execute(cmds, "Web Browser", False, 0, is_kill, user_answering))
                if h.check_noun_lemma("office") and h.check_noun_lemma("suite"):
                    cmds = [{'distro': 'All', 'name': ["libreoffice"]}]
                    return userin.say(userin.execute(cmds, "LibreOffice", False, 0, is_kill, user_answering))
                if h.check_text("draw"):
                    cmds = [{'distro': 'All', 'name': ["libreoffice", "--draw"]}]
                    return userin.say(userin.execute(cmds, "LibreOffice Draw", False, 0, is_kill, user_answering))
                if h.check_text("impress"):
                    cmds = [{'distro': 'All', 'name': ["libreoffice", "--impress"]}]
                    return userin.say(userin.execute(cmds, "LibreOffice Impress", False, 0, is_kill, user_answering))
                if h.check_text("math"):
                    cmds = [{'distro': 'All', 'name': ["libreoffice", "--math"]}]
                    return userin.say(userin.execute(cmds, "LibreOffice Math", False, 0, is_kill, user_answering))
                if h.check_text("writer"):
                    cmds = [{'distro': 'All', 'name': ["libreoffice", "--writer"]}]
                    return userin.say(userin.execute(cmds, "LibreOffice Writer", False, 0, is_kill, user_answering))
            else:
                if h.check_noun_lemma("browser") or h.check_text("chrome") or h.check_text("firefox"):
                    # THESE LINES SPECIAL FOR DETECTING AND KILLING DEFAULT BROWSER.
                    browser_killer_cmds = ["firefox", "chromium-browse", "chrome", "opera", "safari"]
                    raw_result = subprocess.check_output(['xdg-settings', 'get', 'default-web-browser'], stderr=subprocess.DEVNULL)
                    default_browser = raw_result.decode().strip().split(".")[0]
                    cmds = [{'distro': 'All', 'name': []}]
                    for killer in browser_killer_cmds:
                        if killer in default_browser:
                            for cmd in cmds:
                                cmd['name'] = [default_browser]
                    return userin.say(userin.execute(cmds, "Web Browser", False, 0, is_kill))
                if h.check_text("draw") or h.check_text("impress") or h.check_text("math") or h.check_text("writer") or (h.check_noun_lemma("office") and h.check_noun_lemma("suite")):
                    cmds = [{'distro': 'All', 'name': ['soffice.bin']}]
                    return userin.say(userin.execute(cmds, "LibreOffice", False, 0, is_kill))

            # Input: CAMERA, CALENDAR, CALCULATOR, STEAM, BLENDER, TERMINAL
            if h.check_noun_lemma("camera"):
                cmds = [{'distro': 'KDE neon', 'name': ['kamoso']}, {'distro': 'elementary OS', 'name': ['snap-photobooth']}, {'distro': 'Ubuntu', 'name': ['cheese']}, {'distro': 'Linux Mint', 'name': ['cheese']}]
                return userin.say(userin.execute(cmds, "Camera", False, 0, is_kill, user_answering))
            if h.check_noun_lemma("calendar"):
                cmds = [{'distro': 'KDE neon', 'name': ['korganizer']}, {'distro': 'elementary OS', 'name': ['maya-calendar']}, {'distro': 'Ubuntu', 'name': ['orage']}, {'distro': 'Linux Mint', 'name': ['gnome-calendar']}]
                return userin.say(userin.execute(cmds, "Calendar", False, 0, is_kill, user_answering))
            if h.check_noun_lemma("calculator"):
                cmds = [{'distro': 'KDE neon', 'name': ['kcalc']}, {'distro': 'elementary OS', 'name': ['pantheon-calculator']}, {'distro': 'Ubuntu', 'name': ['gnome-calculator']}, {'distro': 'Linux Mint', 'name': ['gnome-calculator']}]
                return userin.say(userin.execute(cmds, "Calculator", False, 0, is_kill, user_answering))
            if h.check_noun_lemma("console"):  # for openin terminal.
                cmds = [{'distro': 'KDE neon', 'name': ['konsole']}, {'distro': 'elementary OS', 'name': ['gnome-terminal']}, {'distro': 'Ubuntu', 'name': ['gnome-terminal']}, {'distro': 'Linux Mint', 'name': ['gnome-terminal']}]
                return userin.say(userin.execute(cmds, "Terminal", False, 0, is_kill, user_answering))
            if h.check_text("blender"):
                cmds = [{'distro': 'All', 'name': ['blender']}]
                return userin.say(userin.execute(cmds, "3D computer graphics software", False, 0, is_kill, user_answering))
            if h.check_text("steam"):
                cmds = [{'distro': 'All', 'name': ['steam']}]
                return userin.say(userin.execute(cmds, "Steam Game Store", False, 0, is_kill, user_answering))

            # Input: GIMP | PHOTOSHOP | PHOTO EDITOR
            if h.check_text("gimp") or (h.check_noun_lemma("photo") and (h.check_noun_lemma("editor") or h.check_noun_lemma("shop"))):
                cmds = [{'distro': 'All', 'name': ['gimp']}]
                return userin.say(userin.execute(cmds, "The photo editor software", False, 0, is_kill, user_answering))

            # Input: INKSCAPE | VECTOR GRAPHICS
            if h.check_text("inkscape") or (h.check_noun_lemma("vector") and h.check_noun_lemma("graphic")) or (h.check_text("vectorial") and h.check_text("drawing")):
                cmds = [{'distro': 'All', 'name': ['inkscape']}]
                return userin.say(userin.execute(cmds, "The vectorial drawing software", False, 0, is_kill, user_answering))

            # Input: Kdenlive | VIDEO EDITOR
            if h.check_text("kdenlive") or (h.check_noun_lemma("video") and h.check_noun_lemma("editor")):
                cmds = [{'distro': 'All', 'name': ['kdenlive']}]
                return userin.say(userin.execute(cmds, "The video editor software", False, 0, is_kill, user_answering))

            # Input FILE MANAGER | FILE EXPLORER
            if h.check_text("files") or (h.check_noun_lemma("file") and h.check_noun_lemma("manager")):
                cmds = [{'distro': 'KDE neon', 'name': ['dolphin']}, {'distro': 'Ubuntu', 'name': ['nautilus']}, {'distro': 'Linux Mint', 'name': ['nemo']}, {'distro': 'elementary OS', 'name': ['pantheon-files']}]
                return userin.say(userin.execute(cmds, "File Manager", False, 0, is_kill, user_answering))

            # Input: SOFTWARE CENTER
            if h.check_noun_lemma("software") and (h.check_text("center") or h.check_text("manager")):
                cmds = [{'distro': 'KDE neon', 'name': ['plasma-discover']}, {'distro': 'Ubuntu', 'name': ['software-center']}, {'distro': 'Linux Mint', 'name': ['mintinstall']}, {'distro': 'elementary OS', 'name': ['software-center']}]
                return userin.say(userin.execute(cmds, "Software Center", False, 0, is_kill, user_answering))

        # Input: MY TITLE IS LADY | I'M A LADY | I'M A WOMAN | I'M A GIRL
        if h.check_lemma("be") and h.check_lemma("-PRON-") and (h.check_lemma("lady") or h.check_lemma("woman") or h.check_lemma("girl")):
            config_file.update({'gender': 'female'}, Query().datatype == 'gender')
            config_file.remove(Query().datatype == 'callme')
            self.user_prefix = GENDER_PREFIX['female']
            user_prefix = self.user_prefix
            return userin.say("Pardon, " + user_prefix + ".")
        # Input: MY TITLE IS SIR | I'M A MAN | I'M A BOY
        if h.check_lemma("be") and h.check_lemma("-PRON-") and (h.check_lemma("sir") or h.check_lemma("man") or h.check_lemma("boy")):
            config_file.update({'gender': 'male'}, Query().datatype == 'gender')
            config_file.remove(Query().datatype == 'callme')
            self.user_prefix = GENDER_PREFIX['male']
            user_prefix = self.user_prefix
            return userin.say("Pardon, " + user_prefix + ".")
        # Input: CALL ME *
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
            self.user_prefix = title
            user_prefix = self.user_prefix
            return userin.say("OK, " + user_prefix + ".")

        # Input: WHAT'S THE TEMPERATURE IN *
        if h.is_wh_question() and h.check_lemma("temperature"):
            city = ""
            for ent in doc.ents:
                if ent.label_ == "GPE":
                    city += ' ' + ent.text
            city = city.strip()
            if city:
                cmds = [{'distro': 'All', 'name': [" "]}]
                owm = pyowm.OWM("16d66c84e82424f0f8e62c3e3b27b574")
                reg = owm.city_id_registry()
                try:
                    weather = owm.weather_at_id(reg.ids_for(city)[0][0]).get_weather()
                    fmt = "The temperature in {} is {} degrees celsius"
                    msg = fmt.format(city, weather.get_temperature('celsius')['temp'])
                    userin.execute(cmds, msg)
                    return userin.say(msg)
                except IndexError:
                    msg = "Sorry, " + user_prefix + " but I couldn't find a city named " + city + " on the internet."
                    userin.execute(cmds, msg)
                    return userin.say(msg)
        # Input: WHAT TIME IS IT
        if h.check_wh_lemma("what") and h.check_noun_lemma("time") and h.check_verb_lemma("be") and h.check_text("it"):
            return userin.say("It's " + datetime.datetime.now().strftime("%I:%M %p") + choice([", " + user_prefix + ".", "."]))

        # Input: KEYBOARD *
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
        # Input: ENTER | NEW TAB | SWITCH TAB | CLOSE | GO BACK | GO FORWARD
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
        # Input: SCROLL LEFT | SCROLL RIGHT | SCROLL UP | SCROLL DOWN
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
        # Input: PLAY | PAUSE | SPACEBAR
        if h.directly_equal(["PLAY", "PAUSE", "SPACEBAR"]) and not args["server"]:
            with nostdout():
                with nostderr():
                    k = PyKeyboard()
                    if not self.testing:
                        k.tap_key(" ")
            return "play"

        # Input: SHUT DOWN THE COMPUTER
        if ((h.check_text("shut") and h.check_text("down")) or (h.check_text("power") and h.check_text("off"))) and h.check_text("computer") and not args["server"]:
            cmds = [{'distro': 'All', 'name': ["gksudo", "poweroff"]}]
            return userin.execute(cmds, "Shutting down", True, 3)
        # Input: GOODBYE | BYE BYE | SEE YOU LATER
        if h.check_nth_lemma(0, "goodbye") or h.check_nth_lemma(0, "bye") or (h.check_verb_lemma("see") and h.check_text("you") and h.check_adv_lemma("later")):
            response = userin.say("Goodbye, " + user_prefix)
            if not args["server"] and not self.testing:
                # raise KeyboardInterrupt
                thread.interrupt_main()
            return response

        # Input: (SEARCH|FIND) * (IN|ON|AT|USING) WIKIPEDIA
        if (h.check_lemma("search") or h.check_lemma("find")) and h.check_lemma("wikipedia"):
            with nostderr():
                search_query = ""
                for token in doc:
                    if not (token.lemma_ == "search" or token.lemma_ == "find" or token.lemma_ == "wikipedia" or token.is_stop):
                        search_query += ' ' + token.text
                search_query = search_query.strip()
                if search_query:
                    try:
                        wikiresult = wikipedia.search(search_query)
                        if len(wikiresult) == 0:
                            userin.say("Sorry, " + user_prefix + ". But I couldn't find anything about " + search_query + " in Wikipedia.")
                            return True
                        wikipage = wikipedia.page(wikiresult[0])
                        wikicontent = "".join([i if ord(i) < 128 else ' ' for i in wikipage.content])
                        wikicontent = re.sub(r'\([^)]*\)', '', wikicontent)
                        cmds = [{'distro': 'All', 'name': ["sensible-browser", wikipage.url]}]
                        userin.execute(cmds, search_query)
                        return userin.say(wikicontent, cmd=["sensible-browser", wikipage.url])
                    except requests.exceptions.ConnectionError:
                        cmds = [{'distro': 'All', 'name': [" "]}]
                        userin.execute(cmds, "Wikipedia connection error.")
                        return userin.say("Sorry, " + user_prefix + ". But I'm unable to connect to Wikipedia servers.")
                    except wikipedia.exceptions.DisambiguationError as disambiguation:
                        user_answering['status'] = True
                        user_answering['for'] = 'wikipedia'
                        user_answering['reason'] = 'disambiguation'
                        user_answering['options'] = disambiguation.options[:3]
                        notify = "Wikipedia disambiguation. Which one of these you meant?:\n - " + disambiguation.options[0]
                        msg = user_prefix + ", there is a disambiguation. Which one of these you meant? " + disambiguation.options[0]
                        for option in disambiguation.options[1:3]:
                            msg += ", or " + option
                            notify += "\n - " + option
                        notify += '\nSay, for example: "THE FIRST ONE" to choose.'
                        cmds = [{'distro': 'All', 'name': [" "]}]
                        userin.execute(cmds, notify)
                        return userin.say(msg)
                    except BaseException:
                        pass
        # Input: (SEARCH|FIND) * (IN|ON|AT|USING) YOUTUBE
        if (h.check_lemma("search") or h.check_lemma("find")) and h.check_lemma("youtube"):
            with nostdout():
                with nostderr():
                    search_query = ""
                    for token in doc:
                        if not (token.lemma_ == "search" or token.lemma_ == "find" or token.lemma_ == "youtube" or token.is_stop):
                            search_query += ' ' + token.text
                    search_query = search_query.strip()
                    if search_query:
                        info = youtube_dl.YoutubeDL({}).extract_info('ytsearch:' + search_query, download=False, ie_key='YoutubeSearch')
                        if len(info['entries']) > 0:
                            youtube_title = info['entries'][0]['title']
                            youtube_url = "https://www.youtube.com/watch?v=%s" % (info['entries'][0]['id'])
                            cmds = [{'distro': 'All', 'name': ["sensible-browser", youtube_url]}]
                            userin.execute(cmds, youtube_title)
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
        # Input: (SEARCH|FIND) * (IN|ON|AT|USING) (GOOGLE|WEB)
        if (h.check_lemma("search") or h.check_lemma("find")) and (h.check_lemma("google") or h.check_lemma("web") or h.check_lemma("internet")) and not h.check_lemma("image"):
            with nostdout():
                with nostderr():
                    search_query = ""
                    for token in doc:
                        if not (token.lemma_ == "search" or token.lemma_ == "find" or token.lemma_ == "google" or token.lemma_ == "web" or token.lemma_ == "internet" or token.is_stop):
                            search_query += ' ' + token.text
                    search_query = search_query.strip()
                    if search_query:
                        tab_url = "http://google.com/?#q=" + search_query
                        cmds = [{'distro': 'All', 'name': ["sensible-browser", tab_url]}]
                        return userin.execute(cmds, search_query, True)
        # Input: (SEARCH IMAGES OF|FIND IMAGES OF|SEARCH|FIND) * (IN|ON|AT|USING) (GOOGLE|WEB|GOOGLE IMAGES|WEB IMAGES)
        if (h.check_lemma("search") or h.check_lemma("find")) and (h.check_lemma("google") or h.check_lemma("web") or h.check_lemma("internet")) and h.check_lemma("image"):
            with nostdout():
                with nostderr():
                    search_query = ""
                    for token in doc:
                        if not (token.lemma_ == "search" or token.lemma_ == "find" or token.lemma_ == "google" or token.lemma_ == "web" or token.lemma_ == "internet" or token.lemma_ == "image" or token.is_stop):
                            search_query += ' ' + token.text
                    search_query = search_query.strip()
                    if search_query:
                        tab_url = "http://google.com/?#q=" + search_query + "&tbm=isch"
                        cmds = [{'distro': 'All', 'name': ["sensible-browser", tab_url]}]
                        return userin.execute(cmds, search_query, True)


        original_com = com
        com = coref.resolve(com)
        if args["verbose"]:
            print("After Coref Resolution: " + com)
        arithmetic_response = arithmetic_parse(com)
        if arithmetic_response:
            return userin.say(arithmetic_response)
        else:
            learner_response = learner.respond(com)
            if learner_response:
                return userin.say(learner_response)
            else:
                omniscient_response = omniscient.respond(com, not args["silent"], userin, user_prefix, args["server"])
                if omniscient_response:
                    return omniscient_response
                else:
                    dc_response = dc.respond(original_com, user_prefix)
                    if dc_response:
                        return userin.say(dc_response)


def tts_kill():
    """The top-level method to kill/end the text-to-speech output immediately.
    """

    subprocess.call(["pkill", "flite"], stdout=FNULL, stderr=FNULL)


def greet(userin):
    """The top-level method to greet the user with message like "*Good morning, sir.*".

    Args:
        userin:  :class:`dragonfire.utilities.TextToAction` instance.

    Returns:
        str:  Response.
    """

    (columns, lines) = shutil.get_terminal_size()
    print(columns * "_" + "\n")
    time = datetime.datetime.now().time()

    global user_full_name
    global user_prefix
    global config_file

    command = "getent passwd $LOGNAME | cut -d: -f5 | cut -d, -f1"
    user_full_name = os.popen(command).read()
    user_full_name = user_full_name[:-1]  # .decode("utf8")
    home = expanduser("~")
    config_file = TinyDB(home + '/.dragonfire_config.json')
    callme_config = config_file.search(Query().datatype == 'callme')
    if callme_config:
        user_prefix = callme_config[0]['title']
    else:
        gender_config = config_file.search(Query().datatype == 'gender')
        if gender_config:
            user_prefix = GENDER_PREFIX[gender_config[0]['gender']]
        else:
            gender = Classifier.gender(user_full_name.split(' ', 1)[0])
            config_file.insert({'datatype': 'gender', 'gender': gender})
            user_prefix = GENDER_PREFIX[gender]

    if datetime.time(4) < time < datetime.time(12):
        time_of_day = "morning"
    elif datetime.time(12) < time < datetime.time(18):
        time_of_day = "afternoon"
    elif datetime.time(18) < time < datetime.time(22):
        time_of_day = "evening"
    else:
        time_of_day = "night"
    cmds = [{'distro': 'All', 'name': ["echo"]}]
    userin.execute(cmds, "To activate say 'Dragonfire!' or 'Wake Up!'")
    return userin.say(" ".join(["Good", time_of_day, user_prefix]))


def speech_error():
    """The top-level method to indicate that there is a speech recognition error occurred.

    Returns:
        str:  Response.
    """

    cmds = [{'distro': 'All', 'name': ["echo"]}]
    userin.execute(cmds, "An error occurred")
    return userin.say("I couldn't understand, please repeat again.")


def initiate():
    """The top-level method to serve as the entry point of Dragonfire.

    This method is the entry point defined in `setup.py` for the `dragonfire` executable that
    placed a directory in `$PATH`.

    This method parses the command-line arguments and handles the top-level initiations accordingly.
    """

    ap = argparse.ArgumentParser()
    ap.add_argument("-c", "--cli", help="Command-line interface mode. Give commands to Dragonfire via command-line inputs (keyboard) instead of audio inputs (microphone).", action="store_true")
    ap.add_argument("-s", "--silent", help="Silent mode. Disable Text-to-Speech output. Dragonfire won't generate any audio output.", action="store_true")
    ap.add_argument("-j", "--headless", help="Headless mode. Do not display an avatar animation on the screen. Disable the female head model.", action="store_true")
    ap.add_argument("-v", "--verbose", help="Increase verbosity of log output.", action="store_true")
    ap.add_argument("-g", "--gspeech", help="Instead of using the default speech recognition method(Mozilla DeepSpeech), use Google Speech Recognition service. (more accurate results)", action="store_true")
    ap.add_argument("--server", help="Server mode. Disable any audio functionality, serve a RESTful spaCy API and become a Twitter integrated chatbot.", metavar="REG_KEY")
    ap.add_argument("-p", "--port", help="Port number for server mode.", default="3301", metavar="PORT")
    ap.add_argument("--version", help="Display the version number of Dragonfire.", action="store_true")
    ap.add_argument("--db", help="Specificy the database engine for the knowledge base of learning feature. Values: 'mysql' for MySQL, 'sqlite' for SQLite. Default database engine is SQLite.", action="store", type=str)
    args = vars(ap.parse_args())
    if args["version"]:
        import pkg_resources
        print(pkg_resources.get_distribution("dragonfire").version)
        sys.exit(1)
    try:
        global dc
        userin = TextToAction(args)
        if not args["server"]:
            SystemTrayExitListenerSet(e)
            stray_proc = Process(target=SystemTrayInit)
            stray_proc.start()
            greet(userin)
        start(args, userin)
    except KeyboardInterrupt:
        if not args["server"]:
            stray_proc.terminate()
        sys.exit(1)


if __name__ == '__main__':
    initiate()
