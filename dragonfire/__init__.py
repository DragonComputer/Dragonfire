#!/usr/bin/python3
# -*- coding: utf-8 -*-

from __future__ import print_function  # , unicode_literals

import argparse
import contextlib

try:
    import cStringIO
except ImportError:
    import io as cStringIO

import datetime
import inspect
import os
import re
import subprocess
import sys

try:
    import thread
except ImportError:
    import _thread as thread

import time
import uuid
from multiprocessing import Event, Process
from os.path import expanduser
from random import choice

import requests.exceptions

import spacy  # Most powerful NLP library available - spaCy
import pyowm
import wikipedia
import wikipedia.exceptions
import youtube_dl
from dragonfire.learn import Learner
from dragonfire.nlplib import Classifier, Helper
from dragonfire.omniscient import Engine
from dragonfire.stray import SystemTrayExitListenerSet, SystemTrayInit
from dragonfire.utilities import TTA
from dragonfire.arithmetic import arithmeticParser
from dragonfire.conversational import DeepConversation
from dragonfire.config import Config
import dragonfire.api as api
from pykeyboard import PyKeyboard
from pymouse import PyMouse
from tinydb import Query, TinyDB

from tweepy.streaming import StreamListener
from tweepy import OAuthHandler
from tweepy import Stream
import tweepy
import json

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


def start(args):

    if args["server"]:
        api.Run(nlp, userin, args["server"])
        if Config.TWITTER_CONSUMER_KEY != 'CONSUMER_KEY':
            auth = OAuthHandler(Config.TWITTER_CONSUMER_KEY, Config.TWITTER_CONSUMER_SECRET)
            auth.set_access_token(Config.TWITTER_ACCESS_KEY, Config.TWITTER_ACCESS_SECRET)
            userin.twitter_api = tweepy.API(auth)

            print("Listening Twitter mentions...")
            l = MentionListener(args)
            stream = Stream(auth, l)
            stream.filter(track=['DragonfireAI'], async=True)
    elif args["cli"]:
        while (True):
            com = raw_input("Enter your command: ")
            thread.start_new_thread(VirtualAssistant.command, (com, args))
            time.sleep(0.5)
    else:
        from dragonfire.sr.deepspeech import DeepSpeechRecognizer
        recognizer = DeepSpeechRecognizer()
        recognizer.recognize(args)


class VirtualAssistant():

    @staticmethod
    def command(com, args, tw_user=None):

        global e
        if (e.is_set()):  # System Tray Icon exit must trigger this
            exit(0)

        if not com.strip() or not isinstance(com, str):
            return False

        original_com = com
        global inactive

        global user_full_name
        global user_prefix
        global config_file

        userin.twitter_user = tw_user

        com = re.sub(r'([^\s\w]|_)+', '', com).strip()
        print("You: " + com.upper())
        doc = nlp(com)
        h = Helper(doc)
        com = com.upper()

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
                            userin.say(wikicontent)
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
        elif (h.check_verb_lemma("go") and h.check_noun_lemma("sleep")) or (h.check_verb_lemma("stop") and h.check_verb_lemma("listen")):
            inactive = True
            userin.execute(["echo"], "Dragonfire deactivated. To reactivate say 'Dragonfire!' or 'Wake Up!'")
            userin.say("I'm going to sleep")
        elif h.directly_equal(["enough"]) or (h.check_verb_lemma("shut") and h.check_nth_lemma(-1, "up")):
            tts_kill()
            print("Dragonfire quiets.")
        elif h.check_wh_lemma("what") and h.check_deps_contains("your name"):
            userin.execute([" "], "My name is Dragonfire.", True)
        elif h.check_wh_lemma("what") and h.check_deps_contains("your gender"):
            userin.say("I have a female voice but I don't have a gender identity. I'm a computer program, " + user_prefix + ".")
        elif (h.check_wh_lemma("who") and h.check_text("I")) or (h.check_verb_lemma("say") and h.check_text("my") and check_lemma("name")):
            userin.execute([" "], user_full_name)
            userin.say("Your name is " + user_full_name + ", " + user_prefix + ".")
        elif h.check_verb_lemma("open") or h.check_adj_lemma("open") or h.check_verb_lemma("run") or h.check_verb_lemma("start") or h.check_verb_lemma("show"):
            if h.check_text("blender"):
                userin.execute(["blender"], "Blender")
                userin.say("Blender 3D computer graphics software")
            elif h.check_text("draw"):
                userin.execute(["libreoffice", "--draw"], "LibreOffice Draw")
                userin.say("Opening LibreOffice Draw")
            elif h.check_text("impress"):
                userin.execute(["libreoffice", "--impress"], "LibreOffice Impress")
                userin.say("Opening LibreOffice Impress")
            elif h.check_text("math"):
                userin.execute(["libreoffice", "--math"], "LibreOffice Math")
                userin.say("Opening LibreOffice Math")
            elif h.check_text("writer"):
                userin.execute(["libreoffice", "--writer"], "LibreOffice Writer")
                userin.say("Opening LibreOffice Writer")
            elif h.check_text("gimp") or (h.check_noun_lemma("photo") and (h.check_noun_lemma("editor") or h.check_noun_lemma("shop"))):
                userin.execute(["gimp"], "GIMP")
                userin.say("Opening the photo editor software.")
            elif h.check_text("inkscape") or (h.check_noun_lemma("vector") and h.check_noun_lemma("graphic")) or (h.check_text("vectorial") and h.check_text("drawing")):
                userin.execute(["inkscape"], "Inkscape")
                userin.say("Opening the vectorial drawing software.")
            elif h.check_noun_lemma("office") and h.check_noun_lemma("suite"):
                userin.execute(["libreoffice"], "LibreOffice")
                userin.say("Opening LibreOffice")
            elif h.check_text("kdenlive") or (h.check_noun_lemma("video") and h.check_noun_lemma("editor")):
                userin.execute(["kdenlive"], "Kdenlive")
                userin.say("Opening the video editor software.")
            elif h.check_noun_lemma("browser") or h.check_noun_lemma("chrome") or h.check_text("firefox"):
                userin.execute(["sensible-browser"], "Web Browser")
                userin.say("Web browser")
            elif h.check_text("steam"):
                userin.execute(["steam"], "Steam")
                userin.say("Opening Steam Game Store")
            elif h.check_text("files") or (h.check_noun_lemma("file") and h.check_noun_lemma("manager")):
                userin.execute(["dolphin"], "File Manager")  # KDE neon
                userin.execute(["pantheon-files"], "File Manager")  # elementary OS
                userin.execute(["nautilus", "--browser"], "File Manager")  # Ubuntu
                userin.say("File Manager")
            elif h.check_noun_lemma("camera"):
                userin.execute(["kamoso"], "Camera")  # KDE neon
                userin.execute(["snap-photobooth"], "Camera")  # elementary OS
                userin.execute(["cheese"], "Camera")  # Ubuntu
                userin.say("Camera")
            elif h.check_noun_lemma("calendar"):
                userin.execute(["korganizer"], "Calendar")  # KDE neon
                userin.execute(["maya-calendar"], "Calendar")  # elementary OS
                userin.execute(["orage"], "Calendar")  # Ubuntu
                userin.say("Calendar")
            elif h.check_noun_lemma("calculator"):
                userin.execute(["kcalc"], "Calculator")  # KDE neon
                userin.execute(["pantheon-calculator"], "Calculator")  # elementary OS
                userin.execute(["gnome-calculator"], "Calculator")  # Ubuntu
                userin.say("Calculator")
            elif h.check_noun_lemma("software") and h.check_text("center"):
                userin.execute(["plasma-discover"], "Software Center")  # KDE neon
                userin.execute(["software-center"], "Software Center")  # elementary OS & Ubuntu
                userin.say("Software Center")
        elif h.check_lemma("be") and h.check_lemma("-PRON-") and (h.check_lemma("lady") or h.check_lemma("woman") or h.check_lemma("girl")):
            config_file.update({'gender': 'female'}, Query().datatype == 'gender')
            config_file.remove(Query().datatype == 'callme')
            user_prefix = "My Lady"
            userin.say("Pardon, " + user_prefix + ".")
        elif h.check_lemma("be") and h.check_lemma("-PRON-") and (h.check_lemma("sir") or h.check_lemma("man") or h.check_lemma("boy")):
            config_file.update({'gender': 'male'}, Query().datatype == 'gender')
            config_file.remove(Query().datatype == 'callme')
            user_prefix = "Sir"
            userin.say("Pardon, " + user_prefix + ".")
        elif h.check_lemma("call") and h.check_lemma("-PRON-"):
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
        # only for The United States today but prepared for all countries. Also
        # only for celsius degrees today. --> by Radan Liska :-)
        elif h.is_wh_question() and h.check_lemma("temperature"):
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
        elif h.check_nth_lemma(0, "keyboard") or h.check_nth_lemma(0, "type"):
            n = len(doc[0].text) + 1
            with nostdout():
                with nostderr():
                    k = PyKeyboard()
                    for character in original_com[n:]:
                        k.tap_key(character)
                    k.tap_key(" ")
        elif h.directly_equal(["enter"]) or (h.check_adj_lemma("new") or h.check_noun_lemma("line")):
            with nostdout():
                with nostderr():
                    k = PyKeyboard()
                    k.tap_key(k.enter_key)
        elif h.check_adj_lemma("new") and h.check_noun_lemma("tab"):
            with nostdout():
                with nostderr():
                    k = PyKeyboard()
                    k.press_keys([k.control_l_key, 't'])
        elif h.check_verb_lemma("switch") and h.check_noun_lemma("tab"):
            with nostdout():
                with nostderr():
                    k = PyKeyboard()
                    k.press_keys([k.control_l_key, k.tab_key])
        elif h.directly_equal(["CLOSE", "ESCAPE"]):
            with nostdout():
                with nostderr():
                    k = PyKeyboard()
                    k.press_keys([k.control_l_key, 'w'])
                    k.tap_key(k.escape_key)
        elif h.check_lemma("back") and h.max_word_count(4):
            with nostdout():
                with nostderr():
                    k = PyKeyboard()
                    k.press_keys([k.alt_l_key, k.left_key])
        elif h.check_lemma("forward") and h.max_word_count(4):
            with nostdout():
                with nostderr():
                    k = PyKeyboard()
                    k.press_keys([k.alt_l_key, k.right_key])
        elif h.check_text("swipe") or h.check_text("scroll"):
            if h.check_text("left"):
                with nostdout():
                    with nostderr():
                        m = PyMouse()
                        m.scroll(0, -5)
            elif h.check_text("right"):
                with nostdout():
                    with nostderr():
                        m = PyMouse()
                        m.scroll(0, 5)
            elif h.check_text("up"):
                with nostdout():
                    with nostderr():
                        m = PyMouse()
                        m.scroll(5, 0)
            elif h.check_text("down"):
                with nostdout():
                    with nostderr():
                        m = PyMouse()
                        m.scroll(-5, 0)
        elif h.directly_equal(["PLAY", "PAUSE", "SPACEBAR"]):
            with nostdout():
                with nostderr():
                    k = PyKeyboard()
                    k.tap_key(" ")
        elif ((h.check_text("shut") and h.check_text("down")) or (h.check_text("power") and h.check_text("off"))) and h.check_text("computer"):
            userin.execute(["sudo", "poweroff"], "Shutting down", True, 3)
        elif h.check_nth_lemma(0, "goodbye") or h.check_nth_lemma(0, "bye") or (h.check_verb_lemma("see") and h.check_noun_lemma("you") and h.check_noun_lemma("later")):
            userin.say("Goodbye, " + user_prefix)
            # raise KeyboardInterrupt
            thread.interrupt_main()
        elif "WIKIPEDIA" in com and ("SEARCH" in com or "FIND" in com):
            with nostderr():
                capture = re.search(
                    "(?:SEARCH|FIND) (?P<query>.*) (?:IN|ON|AT|USING)? WIKIPEDIA", com)
                if capture:
                    search_query = capture.group('query')
                    try:
                        wikiresult = wikipedia.search(search_query)
                        if len(wikiresult) == 0:
                            userin.say("Sorry, " + user_prefix + ". But I couldn't find anything about " + search_query + " in Wikipedia.")
                            return True
                        wikipage = wikipedia.page(wikiresult[0])
                        wikicontent = "".join([i if ord(i) < 128 else ' ' for i in wikipage.content])
                        wikicontent = re.sub(r'\([^)]*\)', '', wikicontent)
                        userin.execute(["sensible-browser", wikipage.url], search_query)
                        userin.say(wikicontent)
                    except requests.exceptions.ConnectionError:
                        userin.execute([" "], "Wikipedia connection error.")
                        userin.say("Sorry, " + user_prefix + ". But I'm unable to connect to Wikipedia servers.")
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
                    except BaseException:
                        pass
        elif "YOUTUBE" in com and ("SEARCH" in com or "FIND" in com):
            with nostdout():
                with nostderr():
                    capture = re.search(
                        "(?:SEARCH|FIND) (?P<query>.*) (?:IN|ON|AT|USING)? YOUTUBE", com)
                    if capture:
                        search_query = capture.group('query')
                        info = youtube_dl.YoutubeDL({}).extract_info('ytsearch:' + search_query, download=False, ie_key='YoutubeSearch')
                        if len(info['entries']) > 0:
                            youtube_title = info['entries'][0]['title']
                            youtube_url = "https://www.youtube.com/watch?v=%s" % (info['entries'][0]['id'])
                            userin.execute(["sensible-browser", youtube_url], youtube_title)
                            youtube_title = "".join([i if ord(i) < 128 else ' ' for i in youtube_title])
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
        elif ("GOOGLE" in com or "WEB" in com) and "IMAGE" not in com and ("SEARCH" in com or "FIND" in com):
            with nostdout():
                with nostderr():
                    capture = re.search(
                        "(?:SEARCH|FIND) (?P<query>.*) (?:IN|ON|AT|USING)? (?:GOOGLE|WEB)?", com)
                    if capture:
                        search_query = capture.group('query')
                        tab_url = "http://google.com/?#q=" + search_query
                        userin.execute(["sensible-browser", tab_url], search_query, True)
        elif ("GOOGLE" in com or "WEB" in com) and "IMAGE" in com and ("SEARCH" in com or "FIND" in com):
            with nostdout():
                with nostderr():
                    capture = re.search("(?:SEARCH IMAGES OF|FIND IMAGES OF|SEARCH|FIND) (?P<query>.*) (?:IN|ON|AT|USING)? (?:GOOGLE|WEB|GOOGLE IMAGES|WEB IMAGES)?", com)
                    if capture:
                        search_query = capture.group('query')
                        tab_url = "http://google.com/?#q=" + search_query + "&tbm=isch"
                        userin.execute(["sensible-browser", tab_url], search_query, True)
        else:
            arithmetic_response = arithmeticParser(com)
            if arithmetic_response:
                userin.say(arithmetic_response)
            else:
                learnerresponse = learner.respond(original_com)
                if learnerresponse:
                    userin.say(learnerresponse)
                else:
                    if not omniscient.respond(original_com, not args["silent"], userin, user_prefix, args["server"]):
                        dc_response = dc.respond(original_com, user_prefix)
                        if dc_response:
                            userin.say(dc_response)


class MentionListener(StreamListener):
    """ A listener handles tweets that are received from the stream.
    This is a basic listener that just prints received tweets to stdout.

    """

    def __init__(self, args):
        self.args = args

    def on_data(self, data):
        global user_full_name
        global user_prefix

        mention = json.loads(data)
        # print(json.dumps(mention, indent=4, sort_keys=True))
        if 'retweeted_status' not in mention:
            tw_text = mention['text']
            tw_user = mention['user']['screen_name']
            if tw_user == "DragonfireAI":
                return True
            user_full_name = mention['user']['name']
            user_prefix = mention['user']['name'].split()[0]
            print("\n@" + tw_user + " said:")
            print(tw_text)
            tw_text = tw_text.replace("@DragonfireAI", "")
            tw_text = re.sub(r'([^\s\w\?]|_)+', '', tw_text).strip()
            thread.start_new_thread(VirtualAssistant.command, (tw_text, self.args, tw_user))
        return True

    def on_error(self, status):
        print(status)


def tts_kill():
    subprocess.call(["pkill", "flite"], stdout=FNULL, stderr=FNULL)


def dragon_greet():
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
    ap.add_argument("--server", help="Server mode. Disable any audio functionality, serve a RESTful spaCy API and become a Twitter integrated chatbot.", metavar="API_KEY")
    ap.add_argument("--version", help="Display the version number of Dragonfire.", action="store_true")
    args = vars(ap.parse_args())
    if args["version"]:
        import pkg_resources
        print(pkg_resources.get_distribution("dragonfire").version)
        sys.exit(1)
    global userin
    userin = TTA(args)
    try:
        global inactive
        global dc
        inactive = False
        if not args["server"]:
            dc = DeepConversation()
            inactive = True
            SystemTrayExitListenerSet(e)
            stray_proc = Process(target=SystemTrayInit)
            stray_proc.start()
            dragon_greet()
        start(args)
    except KeyboardInterrupt:
        if not args["server"]:
            stray_proc.terminate()
        sys.exit(1)


if __name__ == '__main__':
    initiate()
