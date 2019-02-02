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

from dragonfire.commands.takenote import TakeNoteCommand
from dragonfire.commands.find_in_wikipedia import FindInWikiCommand
from dragonfire.commands.direct_cli_execute import CliExecuteCommands
from dragonfire.commands.find_in_youtube import FindInYoutubeCommand
from dragonfire.commands.find_in_browser import FindInBrowserCommand
from dragonfire.commands.keyboard import KeyboardCommands
from dragonfire.commands.set_user_title import SetUserTitleCommands

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
GENDER_PREFIX = {'male': 'Sir', 'female': 'My Lady'}
CONVERSATION_ID = uuid.uuid4()
userin = None
nlp = spacy.load('en')  # Load en_core_web_sm, English, 50 MB, default model
learner = Learner(nlp)
noteTaker = NoteTaker()
omniscient = Omniscient(nlp)
dc = DeepConversation()
coref = NeuralCoref()
e = Event()

takeNoteCommand = TakeNoteCommand()
findInWikiCommand = FindInWikiCommand()
findInYoutubeCommand = FindInYoutubeCommand()
findInBrowserCommand = FindInBrowserCommand()
cliExecuteCommands = CliExecuteCommands()
keyboardCommands = KeyboardCommands()
setUserTitleCommands = SetUserTitleCommands()

USER_ANSWERING_WIKI = {      # user answering for wikipedia search
    'status': False,
    'for': None,
    'reason': None,
    'options': None
}

USER_ANSWERING_NOTE = {     # user answering for taking notes.
    'status': False,
    'isRemind': False,
    'isTodo': False,          # using taking and getting notes both.
    'toDo_listname': None,
    'toDo_listcount': 0,
    'note_keeper': None,
    'has_listname': True
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

        if self.inactive and not (h.directly_equal(["dragonfire", "hey"]) or (h.check_verb_lemma("wake") and h.check_nth_lemma(-1, "up")) or (h.check_nth_lemma(0, "dragon") and h.check_nth_lemma(1, "fire") and h.max_word_count(2))):
            return ""

        response = takeNoteCommand.takenote_compare2(com, noteTaker, USER_ANSWERING_NOTE, userin, user_prefix)   #take note command.
        if response:
            return response

        response = takeNoteCommand.getnote_compare2(com, noteTaker, USER_ANSWERING_NOTE, userin, user_prefix)
        if response:
            return response

        response = findInWikiCommand.second_compare(com, USER_ANSWERING_WIKI, userin, user_prefix)
        if response:
            return response

        if h.directly_equal(["dragonfire", "hey"]) or (h.check_verb_lemma("wake") and h.check_nth_lemma(-1, "up")) or (h.check_nth_lemma(0, "dragon") and h.check_nth_lemma(1, "fire") and h.max_word_count(2)):
            self.inactive = False
            return userin.say(choice([
                "Yes, " + user_prefix + ".",
                "Yes. I'm waiting.",
                "What is your order?",
                "Ready for the orders!",
                user_prefix.capitalize() + ", tell me your wish."
            ]))
        if (h.check_verb_lemma("go") and h.check_noun_lemma("sleep")) or (h.check_verb_lemma("stop") and h.check_verb_lemma("listen")):
            self.inactive = True
            userin.execute(["echo"], "Dragonfire deactivated. To reactivate say 'Dragonfire!' or 'Wake Up!'")
            return userin.say("I'm going to sleep")
        if h.directly_equal(["enough"]) or (h.check_verb_lemma("shut") and h.check_nth_lemma(-1, "up")):
            tts_kill()
            msg = "Dragonfire quiets."
            print(msg)
            return msg
        if h.check_wh_lemma("what") and h.check_deps_contains("your name"):
            return userin.execute([" "], "My name is Dragonfire.", True)
        if h.check_wh_lemma("what") and h.check_deps_contains("your gender"):
            return userin.say("I have a female voice but I don't have a gender identity. I'm a computer program, " + user_prefix + ".")
        if (h.check_wh_lemma("who") and h.check_text("I")) or (h.check_verb_lemma("say") and h.check_text("my") and h.check_lemma("name")):
            userin.execute([" "], user_full_name)
            return userin.say("Your name is " + user_full_name + ", " + user_prefix + ".")

        if (h.check_verb_lemma("what") and h.check_deps_contains("the time")) or h.check_noun_lemma("time") or (
                h.check_verb_lemma("get") or h.check_verb_lemma("say") and h.check_deps_contains("the time")) or (
                h.check_verb_lemma("what") and h.check_noun_lemma("time") and h.check_text("it")):
            takenote_query = ""
            for token in doc:
                if not (token.lemma_ == "what" or token.lemma_ == "time" or token.lemma_ == "get" or token.lemma_ == "say" or token.lemma_ == "it" or token.is_stop):
                    takenote_query += ' ' + token.text
            takenote_query = takenote_query.strip()
            if not takenote_query:                                             # for filter of other sentences.
                atthemoment = datetime.datetime.now().strftime("%H:%M")
                return userin.say(atthemoment + choice([", "+user_prefix + ".", "."]))

        response = takeNoteCommand.getnote_compare1(com, noteTaker, USER_ANSWERING_NOTE, userin, user_prefix)
        if response:
            return response

        response = cliExecuteCommands.compare(com, userin, user_prefix)
        if response:
            return response

        response = takeNoteCommand.takenote_compare1(com, noteTaker, USER_ANSWERING_NOTE, userin, user_prefix)  #take note command
        if response:
            return response

        response = setUserTitleCommands.compare(com, args, userin, config_file)
        if response:
            return response

        if h.is_wh_question() and h.check_lemma("temperature"):
            city = ""
            for ent in doc.ents:
                if ent.label_ == "GPE":
                    city += ' ' + ent.text
            city = city.strip()
            if city:
                owm = pyowm.OWM("16d66c84e82424f0f8e62c3e3b27b574")
                reg = owm.city_id_registry()
                try:
                    weather = owm.weather_at_id(reg.ids_for(city)[0][0]).get_weather()
                    fmt = "The temperature in {} is {} degrees celsius"
                    msg = fmt.format(city, weather.get_temperature('celsius')['temp'])
                    userin.execute([" "], msg)
                    return userin.say(msg)
                except IndexError:
                    msg = "Sorry, " + user_prefix + " but I couldn't find a city named " + city + " on the internet."
                    userin.execute([" "], msg)
                    return userin.say(msg)

        response = keyboardCommands.compare(com, args, self.testing)
        if response:
            return response

        if ((h.check_text("shut") and h.check_text("down")) or (h.check_text("power") and h.check_text("off"))) and h.check_text("computer") and not args["server"]:
            return userin.execute(["sudo", "poweroff"], "Shutting down", True, 3)
        if h.check_nth_lemma(0, "goodbye") or h.check_nth_lemma(0, "bye") or (h.check_verb_lemma("see") and h.check_text("you") and h.check_adv_lemma("later")):
            response = userin.say("Goodbye, " + user_prefix)
            if not args["server"] and not self.testing:
                # raise KeyboardInterrupt
                thread.interrupt_main()
            return response

        response = findInWikiCommand.first_compare(com, USER_ANSWERING_WIKI, userin, user_prefix)
        if response:
            return response

        response = findInYoutubeCommand.compare(com, args, self.testing, userin, user_prefix)
        if response:
            return response

        response = findInBrowserCommand.compare_content(com, userin, user_prefix)
        if response:
            return response

        response = findInBrowserCommand.compare_image(com, userin, user_prefix)
        if response:
            return response

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
    userin.execute(["echo"], "To activate say 'Dragonfire!' or 'Wake Up!'")
    return userin.say(" ".join(["Good", time_of_day, user_prefix]))


def speech_error():
    """The top-level method to indicate that there is a speech recognition error occurred.

    Returns:
        str:  Response.
    """

    userin.execute(["echo"], "An error occurred")
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
