#!/usr/bin/python3
# -*- coding: utf-8 -*-

import argparse  # Parser for command-line options, arguments and sub-commands
import contextlib  # Utilities for with-statement contexts

try:
    import cStringIO  # Read and write strings as files
except ImportError:
    import io as cStringIO  # Read and write strings as files

import datetime  # Basic date and time types
import inspect  # Inspect live objects
import os  # Miscellaneous operating system interfaces
import re  # Regular expression operations
import subprocess  # Subprocess managements
import sys  # System-specific parameters and functions

try:
    import thread  # Low-level threading API
except ImportError:
    import _thread as thread  # Low-level threading API

import time  # Time access and conversions
import uuid  # UUID objects according to RFC 4122
from multiprocessing import Event, Process  # Process-based “threading” interface
from os.path import expanduser  # Common pathname manipulations
from random import choice  # Generate pseudo-random numbers

from dragonfire.learn import Learner  # Submodule of Dragonfire that forms her learning ability
from dragonfire.nlplib import Classifier, Helper  # Submodule of Dragonfire to handle extra NLP tasks
from dragonfire.omniscient import Engine  # Submodule of Dragonfire that serves as a Question Answering Engine
from dragonfire.stray import SystemTrayExitListenerSet, SystemTrayInit  # Submodule of Dragonfire for System Tray Icon related functionalities
from dragonfire.utilities import TextToAction  # Submodule of Dragonfire to provide various utilities
from dragonfire.arithmetic import arithmetic_parse  # Submodule of Dragonfire to analyze arithmetic expressions
from dragonfire.conversational import DeepConversation  # Submodule of Dragonfire to answer questions directly using an Artificial Neural Network
from dragonfire.config import Config  # Submodule of Dragonfire to store configurations

import spacy  # Industrial-strength Natural Language Processing in Python
import pyowm  # A Python wrapper around the OpenWeatherMap API
import wikipedia  # Python library that makes it easy to access and parse data from Wikipedia
import wikipedia.exceptions  # Exceptions of wikipedia library
import requests.exceptions  # HTTP for Humans
import youtube_dl  # Command-line program to download videos from YouTube.com and other video sites
from pykeyboard import PyKeyboard  # A simple, cross-platform Python module for providing keyboard control
from pymouse import PyMouse  # Cross-platform Python mouse module
from tinydb import Query, TinyDB  # TinyDB is a lightweight document oriented database optimized for your happiness


DRAGONFIRE_PATH = os.path.dirname(os.path.abspath(inspect.getfile(inspect.currentframe())))
FNULL = open(os.devnull, 'w')
GENDER_PREFIX = {'male': 'Sir', 'female': 'My Lady'}
CONVERSATION_ID = uuid.uuid4()
userin = None
nlp = spacy.load('en')  # Load en_core_web_sm, English, 50 MB, default model
learner = Learner(nlp)
omniscient = Engine(nlp)
dc = None
e = Event()

USER_ANSWERING = {
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

    if args["server"]:
        import dragonfire.api as api  # API of Dragonfire
        import tweepy  # An easy-to-use Python library for accessing the Twitter API
        from tweepy import OAuthHandler
        from tweepy import Stream
        from dragonfire.tweepy import MentionListener

        if Config.TWITTER_CONSUMER_KEY != 'CONSUMER_KEY':
            auth = OAuthHandler(Config.TWITTER_CONSUMER_KEY, Config.TWITTER_CONSUMER_SECRET)
            auth.set_access_token(Config.TWITTER_ACCESS_KEY, Config.TWITTER_ACCESS_SECRET)
            userin.twitter_api = tweepy.API(auth)

            print("Listening Twitter mentions...")
            l = MentionListener(args, userin)
            stream = Stream(auth, l)
            stream.filter(track=['DragonfireAI'], async=True)
        api.Run(nlp, userin, args["server"], args["port"])
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

            recognizer = GspeechRecognizer()
            recognizer.recognize(args, userin, user_full_name, user_prefix)
        else:
            from dragonfire.sr.deepspeech import DeepSpeechRecognizer

            recognizer = DeepSpeechRecognizer()
            recognizer.recognize(args, userin, user_full_name, user_prefix)


class VirtualAssistant():

    def __init__(self, args, userin, user_full_name="John Doe", user_prefix="sir", tw_user=None):
        self.args = args
        self.userin = userin
        self.user_full_name = user_full_name
        self.user_prefix = user_prefix
        self.userin.twitter_user = tw_user

    def command(self, com):

        if not self.args["server"]:
            global inactive
            global config_file
            global e
            if (e.is_set()):  # System Tray Icon exit must trigger this
                exit(0)
        args = self.args
        userin = self.userin
        user_full_name = self.user_full_name
        user_prefix = self.user_prefix

        if not com.strip() or not isinstance(com, str):
            return False

        print("You: " + com.upper())
        doc = nlp(com)
        h = Helper(doc)

        if args["verbose"]:
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

        if inactive and not (h.directly_equal(["dragonfire", "hey"]) or (h.check_verb_lemma("wake") and h.check_nth_lemma(-1, "up")) or (h.check_nth_lemma(0, "dragon") and h.check_nth_lemma(1, "fire") and h.max_word_count(2))):
            return True

        if USER_ANSWERING['status']:
            if com.startswith("FIRST") or com.startswith("THE FIRST") or com.startswith("SECOND") or com.startswith("THE SECOND") or com.startswith("THIRD") or com.startswith("THE THIRD"):
                USER_ANSWERING['status'] = False
                selection = None
                if com.startswith("FIRST") or com.startswith("THE FIRST"):
                    selection = 0
                elif com.startswith("SECOND") or com.startswith("THE SECOND"):
                    selection = 1
                elif com.startswith("THIRD") or com.startswith("THE THIRD"):
                    selection = 2

                if USER_ANSWERING['for'] == 'wikipedia':
                    with nostderr():
                        search_query = USER_ANSWERING['options'][selection]
                        try:
                            wikiresult = wikipedia.search(search_query)
                            if len(wikiresult) == 0:
                                userin.say("Sorry, " + user_prefix + ". But I couldn't find anything about " + search_query + " in Wikipedia.")
                                return True
                            wikipage = wikipedia.page(wikiresult[0])
                            wikicontent = "".join([i if ord(i) < 128 else ' ' for i in wikipage.content])
                            wikicontent = re.sub(r'\([^)]*\)', '', wikicontent)
                            userin.execute(["sensible-browser", wikipage.url], search_query)
                            userin.say(wikicontent, cmd=["sensible-browser", wikipage.url])
                            return True
                        except requests.exceptions.ConnectionError:
                            userin.execute([" "], "Wikipedia connection error.")
                            userin.say("Sorry, " + user_prefix + ". But I'm unable to connect to Wikipedia servers.")
                            return True
                        except Exception:
                            return True

        if h.directly_equal(["dragonfire", "hey"]) or (h.check_verb_lemma("wake") and h.check_nth_lemma(-1, "up")) or (h.check_nth_lemma(0, "dragon") and h.check_nth_lemma(1, "fire") and h.max_word_count(2)):
            inactive = False
            userin.say(choice([
                "Yes, " + user_prefix + ".",
                "Yes. I'm waiting.",
                "What is your order?",
                "Ready for the orders!",
                user_prefix + ", tell me your wish."
            ]))
            return True
        if (h.check_verb_lemma("go") and h.check_noun_lemma("sleep")) or (h.check_verb_lemma("stop") and h.check_verb_lemma("listen")):
            inactive = True
            userin.execute(["echo"], "Dragonfire deactivated. To reactivate say 'Dragonfire!' or 'Wake Up!'")
            userin.say("I'm going to sleep")
            return True
        if h.directly_equal(["enough"]) or (h.check_verb_lemma("shut") and h.check_nth_lemma(-1, "up")):
            tts_kill()
            print("Dragonfire quiets.")
            return True
        if h.check_wh_lemma("what") and h.check_deps_contains("your name"):
            userin.execute([" "], "My name is Dragonfire.", True)
            return True
        if h.check_wh_lemma("what") and h.check_deps_contains("your gender"):
            userin.say("I have a female voice but I don't have a gender identity. I'm a computer program, " + user_prefix + ".")
            return True
        if (h.check_wh_lemma("who") and h.check_text("I")) or (h.check_verb_lemma("say") and h.check_text("my") and check_lemma("name")):
            userin.execute([" "], user_full_name)
            userin.say("Your name is " + user_full_name + ", " + user_prefix + ".")
            return True
        if h.check_verb_lemma("open") or h.check_adj_lemma("open") or h.check_verb_lemma("run") or h.check_verb_lemma("start") or h.check_verb_lemma("show"):
            if h.check_text("blender"):
                userin.execute(["blender"], "Blender")
                userin.say("Blender 3D computer graphics software")
                return True
            if h.check_text("draw"):
                userin.execute(["libreoffice", "--draw"], "LibreOffice Draw")
                userin.say("Opening LibreOffice Draw")
                return True
            if h.check_text("impress"):
                userin.execute(["libreoffice", "--impress"], "LibreOffice Impress")
                userin.say("Opening LibreOffice Impress")
                return True
            if h.check_text("math"):
                userin.execute(["libreoffice", "--math"], "LibreOffice Math")
                userin.say("Opening LibreOffice Math")
                return True
            if h.check_text("writer"):
                userin.execute(["libreoffice", "--writer"], "LibreOffice Writer")
                userin.say("Opening LibreOffice Writer")
                return True
            if h.check_text("gimp") or (h.check_noun_lemma("photo") and (h.check_noun_lemma("editor") or h.check_noun_lemma("shop"))):
                userin.execute(["gimp"], "GIMP")
                userin.say("Opening the photo editor software.")
                return True
            if h.check_text("inkscape") or (h.check_noun_lemma("vector") and h.check_noun_lemma("graphic")) or (h.check_text("vectorial") and h.check_text("drawing")):
                userin.execute(["inkscape"], "Inkscape")
                userin.say("Opening the vectorial drawing software.")
                return True
            if h.check_noun_lemma("office") and h.check_noun_lemma("suite"):
                userin.execute(["libreoffice"], "LibreOffice")
                userin.say("Opening LibreOffice")
                return True
            if h.check_text("kdenlive") or (h.check_noun_lemma("video") and h.check_noun_lemma("editor")):
                userin.execute(["kdenlive"], "Kdenlive")
                userin.say("Opening the video editor software.")
                return True
            if h.check_noun_lemma("browser") or h.check_noun_lemma("chrome") or h.check_text("firefox"):
                userin.execute(["sensible-browser"], "Web Browser")
                userin.say("Web browser")
                return True
            if h.check_text("steam"):
                userin.execute(["steam"], "Steam")
                userin.say("Opening Steam Game Store")
                return True
            if h.check_text("files") or (h.check_noun_lemma("file") and h.check_noun_lemma("manager")):
                userin.execute(["dolphin"], "File Manager")  # KDE neon
                userin.execute(["pantheon-files"], "File Manager")  # elementary OS
                userin.execute(["nautilus", "--browser"], "File Manager")  # Ubuntu
                userin.say("File Manager")
                return True
            if h.check_noun_lemma("camera"):
                userin.execute(["kamoso"], "Camera")  # KDE neon
                userin.execute(["snap-photobooth"], "Camera")  # elementary OS
                userin.execute(["cheese"], "Camera")  # Ubuntu
                userin.say("Camera")
                return True
            if h.check_noun_lemma("calendar"):
                userin.execute(["korganizer"], "Calendar")  # KDE neon
                userin.execute(["maya-calendar"], "Calendar")  # elementary OS
                userin.execute(["orage"], "Calendar")  # Ubuntu
                userin.say("Calendar")
                return True
            if h.check_noun_lemma("calculator"):
                userin.execute(["kcalc"], "Calculator")  # KDE neon
                userin.execute(["pantheon-calculator"], "Calculator")  # elementary OS
                userin.execute(["gnome-calculator"], "Calculator")  # Ubuntu
                userin.say("Calculator")
                return True
            if h.check_noun_lemma("software") and h.check_text("center"):
                userin.execute(["plasma-discover"], "Software Center")  # KDE neon
                userin.execute(["software-center"], "Software Center")  # elementary OS & Ubuntu
                userin.say("Software Center")
                return True
        if h.check_lemma("be") and h.check_lemma("-PRON-") and (h.check_lemma("lady") or h.check_lemma("woman") or h.check_lemma("girl")):
            config_file.update({'gender': 'female'}, Query().datatype == 'gender')
            config_file.remove(Query().datatype == 'callme')
            user_prefix = "My Lady"
            userin.say("Pardon, " + user_prefix + ".")
            return True
        if h.check_lemma("be") and h.check_lemma("-PRON-") and (h.check_lemma("sir") or h.check_lemma("man") or h.check_lemma("boy")):
            config_file.update({'gender': 'male'}, Query().datatype == 'gender')
            config_file.remove(Query().datatype == 'callme')
            user_prefix = "Sir"
            userin.say("Pardon, " + user_prefix + ".")
            return True
        if h.check_lemma("call") and h.check_lemma("-PRON-"):
            title = ""
            for token in doc:
                if token.pos_ == "NOUN":
                    title += ' ' + token.text
            title = title.strip()
            callme_config = config_file.search(Query().datatype == 'callme')
            if callme_config:
                config_file.update({'title': title}, Query().datatype == 'callme')
            else:
                config_file.insert({'datatype': 'callme', 'title': title})
            user_prefix = title
            userin.say("OK, " + user_prefix + ".")
            return True
        # only for The United States today but prepared for all countries. Also
        # only for celsius degrees today. --> by Radan Liska :-)
        if h.is_wh_question() and h.check_lemma("temperature"):
            city = ""
            for ent in doc.ents:
                if ent.label_ == "GPE":
                    city += ' ' + ent.text
            city = city.strip()
            if city:
                owm = pyowm.OWM("16d66c84e82424f0f8e62c3e3b27b574")
                reg = owm.city_id_registry()
                weather = owm.weather_at_id(reg.ids_for(city)[0][0]).get_weather()
                fmt = "The temperature in {} is {} degrees celsius"
                msg = fmt.format(city, weather.get_temperature('celsius')['temp'])
                userin.execute([" "], msg)
                userin.say(msg)
                return True
        if h.check_nth_lemma(0, "keyboard") or h.check_nth_lemma(0, "type"):
            n = len(doc[0].text) + 1
            with nostdout():
                with nostderr():
                    k = PyKeyboard()
                    for character in com[n:]:
                        k.tap_key(character)
                    k.tap_key(" ")
            return True
        if h.directly_equal(["enter"]) or (h.check_adj_lemma("new") or h.check_noun_lemma("line")):
            with nostdout():
                with nostderr():
                    k = PyKeyboard()
                    k.tap_key(k.enter_key)
            return True
        if h.check_adj_lemma("new") and h.check_noun_lemma("tab"):
            with nostdout():
                with nostderr():
                    k = PyKeyboard()
                    k.press_keys([k.control_l_key, 't'])
            return True
        if h.check_verb_lemma("switch") and h.check_noun_lemma("tab"):
            with nostdout():
                with nostderr():
                    k = PyKeyboard()
                    k.press_keys([k.control_l_key, k.tab_key])
            return True
        if h.directly_equal(["CLOSE", "ESCAPE"]):
            with nostdout():
                with nostderr():
                    k = PyKeyboard()
                    k.press_keys([k.control_l_key, 'w'])
                    k.tap_key(k.escape_key)
            return True
        if h.check_lemma("back") and h.max_word_count(4):
            with nostdout():
                with nostderr():
                    k = PyKeyboard()
                    k.press_keys([k.alt_l_key, k.left_key])
            return True
        if h.check_lemma("forward") and h.max_word_count(4):
            with nostdout():
                with nostderr():
                    k = PyKeyboard()
                    k.press_keys([k.alt_l_key, k.right_key])
            return True
        if h.check_text("swipe") or h.check_text("scroll"):
            if h.check_text("left"):
                with nostdout():
                    with nostderr():
                        m = PyMouse()
                        m.scroll(0, -5)
                return True
            if h.check_text("right"):
                with nostdout():
                    with nostderr():
                        m = PyMouse()
                        m.scroll(0, 5)
                return True
            if h.check_text("up"):
                with nostdout():
                    with nostderr():
                        m = PyMouse()
                        m.scroll(5, 0)
                return True
            if h.check_text("down"):
                with nostdout():
                    with nostderr():
                        m = PyMouse()
                        m.scroll(-5, 0)
                return True
        if h.directly_equal(["PLAY", "PAUSE", "SPACEBAR"]):
            with nostdout():
                with nostderr():
                    k = PyKeyboard()
                    k.tap_key(" ")
            return True
        if ((h.check_text("shut") and h.check_text("down")) or (h.check_text("power") and h.check_text("off"))) and h.check_text("computer"):
            userin.execute(["sudo", "poweroff"], "Shutting down", True, 3)
            return True
        if h.check_nth_lemma(0, "goodbye") or h.check_nth_lemma(0, "bye") or (h.check_verb_lemma("see") and h.check_noun_lemma("you") and h.check_noun_lemma("later")):
            userin.say("Goodbye, " + user_prefix)
            # raise KeyboardInterrupt
            thread.interrupt_main()
            return True
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
                        userin.execute(["sensible-browser", wikipage.url], search_query)
                        userin.say(wikicontent, cmd=["sensible-browser", wikipage.url])
                        return True
                    except requests.exceptions.ConnectionError:
                        userin.execute([" "], "Wikipedia connection error.")
                        userin.say("Sorry, " + user_prefix + ". But I'm unable to connect to Wikipedia servers.")
                        return True
                    except wikipedia.exceptions.DisambiguationError as disambiguation:
                        USER_ANSWERING['status'] = True
                        USER_ANSWERING['for'] = 'wikipedia'
                        USER_ANSWERING['reason'] = 'disambiguation'
                        USER_ANSWERING['options'] = disambiguation.options[:3]
                        notify = "Wikipedia disambiguation. Which one of these you meant?:\n - " + disambiguation.options[0]
                        message = user_prefix + ", there is a disambiguation. Which one of these you meant? " + disambiguation.options[0]
                        for option in disambiguation.options[1:3]:
                            message += ", or " + option
                            notify += "\n - " + option
                        notify += '\nSay, for example: "THE FIRST ONE" to choose.'
                        userin.execute([" "], notify)
                        userin.say(message)
                        return True
                    except BaseException:
                        pass
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
                            userin.execute(["sensible-browser", youtube_url], youtube_title)
                            youtube_title = "".join([i if ord(i) < 128 else ' ' for i in youtube_title])
                            userin.say(youtube_title, ["sensible-browser", youtube_url])
                        else:
                            youtube_title = "No video found, " + user_prefix + "."
                            userin.say(youtube_title)
                        time.sleep(5)
                        k = PyKeyboard()
                        k.tap_key(k.tab_key)
                        k.tap_key(k.tab_key)
                        k.tap_key(k.tab_key)
                        k.tap_key(k.tab_key)
                        k.tap_key('f')
                        return True
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
                        userin.execute(["sensible-browser", tab_url], search_query, True)
                        return True
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
                        userin.execute(["sensible-browser", tab_url], search_query, True)
                        return True

        arithmetic_response = arithmetic_parse(com)
        if arithmetic_response:
            userin.say(arithmetic_response)
        else:
            learnerresponse = learner.respond(com)
            if learnerresponse:
                userin.say(learnerresponse)
            else:
                if not omniscient.respond(com, not args["silent"], userin, user_prefix, args["server"]):
                    dc_response = dc.respond(com, user_prefix)
                    if dc_response:
                        userin.say(dc_response)


def tts_kill():
    subprocess.call(["pkill", "flite"], stdout=FNULL, stderr=FNULL)


def dragon_greet(userin):
    print("_______________________________________________________________\n")
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

    if time < datetime.time(12):
        time_of_day = "morning"
    elif datetime.time(12) < time < datetime.time(18):
        time_of_day = "afternoon"
    else:
        time_of_day = "evening"
    userin.execute(["echo"], "To activate say 'Dragonfire!' or 'Wake Up!'")
    userin.say(" ".join(["Good", time_of_day, user_prefix]))


def speech_error():
    userin.execute(["echo"], "An error occurred")
    userin.say("I couldn't understand, please repeat again.")


@contextlib.contextmanager
def nostdout():
    save_stdout = sys.stdout
    sys.stdout = cStringIO.StringIO()
    yield
    sys.stdout = save_stdout


@contextlib.contextmanager
def nostderr():
    save_stderr = sys.stderr
    sys.stderr = cStringIO.StringIO()
    yield
    sys.stderr = save_stderr


def initiate():
    ap = argparse.ArgumentParser()
    ap.add_argument("-c", "--cli", help="Command-line interface mode. Give commands to Dragonfire via command-line inputs (keyboard) instead of audio inputs (microphone).", action="store_true")
    ap.add_argument("-s", "--silent", help="Silent mode. Disable Text-to-Speech output. Dragonfire won't generate any audio output.", action="store_true")
    ap.add_argument("-j", "--headless", help="Headless mode. Do not display an avatar animation on the screen. Disable the female head model.", action="store_true")
    ap.add_argument("-v", "--verbose", help="Increase verbosity of log output.", action="store_true")
    ap.add_argument("-g", "--gspeech", help="Instead of using the default speech recognition method(Mozilla DeepSpeech), use Google Speech Recognition service. (more accurate results)", action="store_true")
    ap.add_argument("--server", help="Server mode. Disable any audio functionality, serve a RESTful spaCy API and become a Twitter integrated chatbot.", metavar="API_KEY")
    ap.add_argument("-p", "--port", help="Port number for server mode.", default="3301", metavar="PORT")
    ap.add_argument("--version", help="Display the version number of Dragonfire.", action="store_true")
    args = vars(ap.parse_args())
    if args["version"]:
        import pkg_resources
        print(pkg_resources.get_distribution("dragonfire").version)
        sys.exit(1)
    try:
        global inactive
        global dc
        inactive = False
        userin = TextToAction(args)
        if not args["server"]:
            dc = DeepConversation()
            inactive = True
            SystemTrayExitListenerSet(e)
            stray_proc = Process(target=SystemTrayInit)
            stray_proc.start()
            dragon_greet(userin)
        start(args, userin)
    except KeyboardInterrupt:
        if not args["server"]:
            stray_proc.terminate()
        sys.exit(1)


if __name__ == '__main__':
    initiate()
