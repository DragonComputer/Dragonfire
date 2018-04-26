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

import pyowm
import wikipedia
import wikipedia.exceptions
import youtube_dl
from dragonfire.learn import Learn
from dragonfire.nlplib import Classifiers
from dragonfire.omniscient import Engine
from dragonfire.stray import SystemTrayExitListenerSet, SystemTrayInit
from dragonfire.utilities import TTA
from pykeyboard import PyKeyboard
from pymouse import PyMouse
from tinydb import Query, TinyDB

DRAGONFIRE_PATH = os.path.dirname(
    os.path.abspath(inspect.getfile(inspect.currentframe())))
FNULL = open(os.devnull, 'w')
GENDER_PREFIX = {'male': 'Sir', 'female': 'My Lady'}
CONVERSATION_ID = uuid.uuid4()
userin = None
learn_ = Learn()
omniscient_ = Engine()
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

    if args["cli"]:
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
    def exact_match(com):  # if key == com: ...
        if com == "WHO AM I":
            com = "SAY MY NAME"
        app_info = {
            "OPEN BLENDER": (["blender"], "Blender",
                             "Blender 3D computer graphics software"),
            "OPEN DRAW": (["libreoffice", "--draw"], "LibreOffice Draw",
                          "Draw"),
            "OPEN IMPRESS": (["libreoffice", "--impress"],
                             "LibreOffice Impress", "Impress"),
            "OPEN MATH": (["libreoffice", "--math"], "LibreOffice Math",
                          "Math"),
            "OPEN STREAM": (["steam"], "Steam", "Steam Game Store"),
            "OPEN WRITER": (["libreoffice", "--writer"], "LibreOffice Writer",
                            "Writer"),
            "SAY MY NAME":
            ([" "], user_full_name,
             "Your name is " + user_full_name + ", " + user_prefix + "."),
            "WHAT IS YOUR GENDER":
            ([" "], " ",
             "I have a female voice but I don't have a gender identity. I'm a computer program, "
             + user_prefix + "."),
            "WHAT IS YOUR NAME": ([" "], "My name is Dragonfire.",
                                  "My name is Dragonfire."),
        }.get(com)
        if app_info:
            tts_kill()
            commands, message, say_text = app_info
            userin.define_and_execute(commands, message)
            userin.say(say_text)
        return bool(app_info)

    @staticmethod
    def in_match(com):  # if key in com: ...
        if "PHOTO SHOP" in com or "PHOTO EDITOR" in com:
            com = "GIMP"
        elif "VECTOR GRAPHICS" in com or "VECTORIAL DRAWING" in com:
            com = "INKSCAPE"
        apps = {
            "GIMP": (["gimp"], "GIMP", "Photo editor"),
            "INKSCAPE": (["inkscape"], "Inkscape", "Inkscape"),
            "OFFICE SUITE": (["libreoffice"], "LibreOffice", "Office Suite"),
            "VIDEO EDITOR": (["kdenlive"], "Kdenlive", "Video editor"),
            "WEB BROWSER": (["sensible-browser"], "Web Browser", "Web Browser")
        }
        for app_name, app_info in apps.items():
            if app_name in com:
                tts_kill()
                commands, message, say_text = app_info
                userin.define_and_execute(commands, message)
                userin.say(say_text)
                return True
        return False

    @staticmethod
    def regex_match(com):  # if re.search(r"string", com): ...
        return False  # not yet implemented

    @staticmethod
    def search_command(com):  # if "SEARCH" in com or "FIND" in com: ...
        assert "SEARCH" in com or "FIND" in com, com
        return False  # not yet implemented

    @staticmethod
    def command(com, args):

        global e
        if (e.is_set()):  # System Tray Icon exit must trigger this
            exit(0)

        if not com or not isinstance(com, str):
            return False

        original_com = com
        global inactive

        global user_full_name
        global user_prefix
        global config_file

        com = com.upper()
        print("You: " + com)

        if inactive and com not in ("DRAGONFIRE", "DRAGON FIRE", "WAKE UP",
                                    "HEY"):
            return True

        if USER_ANSWERING['status']:
            if com.startswith("FIRST") or com.startswith(
                    "THE FIRST") or com.startswith("SECOND") or com.startswith(
                        "THE SECOND") or com.startswith(
                            "THIRD") or com.startswith("THE THIRD"):
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
                                userin.say(
                                    "Sorry, " + user_prefix +
                                    ". But I couldn't find anything about " +
                                    search_query + " in Wikipedia.")
                                return True
                            wikipage = wikipedia.page(wikiresult[0])
                            wikicontent = "".join([
                                i if ord(i) < 128 else ' '
                                for i in wikipage.content
                            ])
                            wikicontent = re.sub(r'\([^)]*\)', '', wikicontent)
                            userin.define_and_execute(
                                ["sensible-browser", wikipage.url],
                                search_query)
                            userin.say(wikicontent)
                            return True
                        except requests.exceptions.ConnectionError:
                            userin.define_and_execute(
                                [" "], "Wikipedia connection error.")
                            userin.say(
                                "Sorry, " +
                                user_prefix +
                                ". But I'm unable to connect to Wikipedia servers.")
                            return True
                        except Exception:
                            return True

        if com in ("DRAGONFIRE", "DRAGON FIRE", "WAKE UP", "HEY"):
            tts_kill()
            inactive = False
            userin.define([" "], " ")
            words_dragonfire = ("Yes, " + user_prefix + ".",
                                "Yes. I'm waiting.", "What is your orders?")
            userin.say(choice(words_dragonfire))
        elif "GO TO SLEEP" == com:
            tts_kill()
            inactive = True
            userin.define_and_execute(
                ["echo"],
                "Dragonfire deactivated. To reactivate say 'Dragonfire!' or 'Wake Up!'")
            userin.say("I'm going to sleep")
        elif com in ("ENOUGH", "SHUT UP"):
            print("Dragonfire quiets.")
            tts_kill()
        elif VirtualAssistant.exact_match(com):
            pass  # the request has been handled
        elif VirtualAssistant.in_match(com):
            pass  # the request has been handled
        elif ("SEARCH" in com
              or "FIND" in com) and VirtualAssistant.search_command(com):
            pass  # the request has been handled
        elif com in ("MY TITLE IS LADY", "I'M A LADY", "I'M A WOMAN",
                     "I'M A GIRL"):
            tts_kill()
            config_file.update({
                'gender': 'female'
            },
                Query().datatype == 'gender')
            user_prefix = "My Lady"
            userin.define([" "], " ")
            userin.say("Pardon, " + user_prefix + ".")
        elif com in ("MY TITLE IS SIR", "I'M A MAN", "I'M A BOY"):
            tts_kill()
            config_file.update({
                'gender': 'male'
            },
                Query().datatype == 'gender')
            user_prefix = "Sir"
            userin.define([" "], " ")
            userin.say("Pardon, " + user_prefix + ".")
        elif com.startswith("CALL ME "):
            tts_kill()
            callme_config = config_file.search(Query().datatype == 'callme')
            if callme_config:
                config_file.update({
                    'title': original_com[8:].lower()
                },
                    Query().datatype == 'callme')
            else:
                config_file.insert({
                    'datatype': 'callme',
                    'title': original_com[8:].lower()
                })
            user_prefix = original_com[8:].lower().encode("utf8")
            userin.define([" "], " ")
            userin.say("Pardon, " + user_prefix + ".")
        # only for The United States today but prepared for all countries. Also
        # only for celsius degrees today. --> by Radan Liska :-)
        elif "WHAT" in com and "TEMPERATURE" in com:
            tts_kill()
            capture = re.search(
                "(?:WHAT IS|WHAT'S) THE TEMPERATURE (?:IN|ON|AT|OF)? (?P<city>.*)", com)
            if capture:
                city = capture.group('city')
                owm = pyowm.OWM("16d66c84e82424f0f8e62c3e3b27b574")
                reg = owm.city_id_registry()
                weather = owm.weather_at_id(
                    reg.ids_for(city)[0][0]).get_weather()
                fmt = "The temperature in {} is {} degrees celsius"
                msg = fmt.format(city,
                                 weather.get_temperature('celsius')['temp'])
                userin.define_and_execute([" "], msg)
                userin.say(msg)
        elif "FILE MANAGER" in com or "OPEN FILES" == com:
            tts_kill()
            userin.define_and_execute(["dolphin"], "File Manager")  # KDE neon
            userin.define_and_execute(["pantheon-files"],
                                      "File Manager")  # elementary OS
            userin.define_and_execute(["nautilus", "--browser"],
                                      "File Manager")  # Ubuntu
            userin.say("File Manager")
        elif "OPEN CAMERA" == com:
            tts_kill()
            userin.define_and_execute(["kamoso"], "Camera")  # KDE neon
            userin.define_and_execute(["snap-photobooth"],
                                      "Camera")  # elementary OS
            userin.define_and_execute(["cheese"], "Camera")  # Ubuntu
            userin.say("Camera")
        elif "OPEN CALENDAR" == com:
            tts_kill()
            userin.define_and_execute(["korganizer"], "Calendar")  # KDE neon
            userin.define_and_execute(["maya-calendar"],
                                      "Calendar")  # elementary OS
            userin.define_and_execute(["orage"], "Calendar")  # Ubuntu
            userin.say("Calendar")
        elif "OPEN CALCULATOR" == com:
            tts_kill()
            userin.define_and_execute(["kcalc"], "Calculator")  # KDE neon
            userin.define_and_execute(["pantheon-calculator"],
                                      "Calculator")  # elementary OS
            userin.define_and_execute(["gnome-calculator"],
                                      "Calculator")  # Ubuntu
            userin.say("Calculator")
        elif "SOFTWARE CENTER" in com:
            tts_kill()
            userin.define_and_execute(["plasma-discover"],
                                      "Software Center")  # KDE neon
            userin.define_and_execute(
                ["software-center"],
                "Software Center")  # elementary OS & Ubuntu
            userin.say("Software Center")
        elif com.startswith("KEYBOARD "):
            tts_kill()
            with nostdout():
                with nostderr():
                    k = PyKeyboard()
                    for character in original_com[9:]:
                        k.tap_key(character)
                    k.tap_key(" ")
        elif com == "ENTER":
            tts_kill()
            with nostdout():
                with nostderr():
                    k = PyKeyboard()
                    k.tap_key(k.enter_key)
        elif com == "NEW TAB":
            tts_kill()
            with nostdout():
                with nostderr():
                    k = PyKeyboard()
                    k.press_keys([k.control_l_key, 't'])
        elif com == "SWITCH TAB":
            tts_kill()
            with nostdout():
                with nostderr():
                    k = PyKeyboard()
                    k.press_keys([k.control_l_key, k.tab_key])
        elif com in ("CLOSE", "ESCAPE"):
            tts_kill()
            with nostdout():
                with nostderr():
                    k = PyKeyboard()
                    k.press_keys([k.control_l_key, 'w'])
                    k.tap_key(k.escape_key)
        elif com == "GO BACK":
            tts_kill()
            with nostdout():
                with nostderr():
                    k = PyKeyboard()
                    k.press_keys([k.alt_l_key, k.left_key])
        elif com == "GO FORWARD":
            tts_kill()
            with nostdout():
                with nostderr():
                    k = PyKeyboard()
                    k.press_keys([k.alt_l_key, k.right_key])
        elif com == "SCROLL LEFT":
            tts_kill()
            with nostdout():
                with nostderr():
                    m = PyMouse()
                    m.scroll(0, -5)
        elif com == "SCROLL RIGHT":
            tts_kill()
            with nostdout():
                with nostderr():
                    m = PyMouse()
                    m.scroll(0, 5)
        elif com == "SCROLL UP":
            tts_kill()
            with nostdout():
                with nostderr():
                    m = PyMouse()
                    m.scroll(5, 0)
        elif com == "SCROLL DOWN":
            tts_kill()
            with nostdout():
                with nostderr():
                    m = PyMouse()
                    m.scroll(-5, 0)
        elif com in ("PLAY", "PAUSE", "SPACEBAR"):
            tts_kill()
            with nostdout():
                with nostderr():
                    k = PyKeyboard()
                    k.tap_key(" ")
        elif "SHUTDOWN THE COMPUTER" == com:
            tts_kill()
            userin.define(["sudo", "poweroff"], "Shutting down")
            userin.say("Shutting down")
            userin.execute(3)
        elif com in ("GOODBYE", "GOOD BYE", "BYE BYE", "SEE YOU LATER", "CATCH YOU LATER"):
            tts_kill()
            userin.define([" "], " ")
            userin.say("Goodbye, " + user_prefix)
            # raise KeyboardInterrupt
            thread.interrupt_main()
        elif "WIKIPEDIA" in com and ("SEARCH" in com or "FIND" in com):
            tts_kill()
            with nostderr():
                capture = re.search(
                    "(?:SEARCH|FIND) (?P<query>.*) (?:IN|ON|AT|USING)? WIKIPEDIA", com)
                if capture:
                    search_query = capture.group('query')
                    try:
                        wikiresult = wikipedia.search(search_query)
                        if len(wikiresult) == 0:
                            userin.say("Sorry, " + user_prefix +
                                       ". But I couldn't find anything about "
                                       + search_query + " in Wikipedia.")
                            return True
                        wikipage = wikipedia.page(wikiresult[0])
                        wikicontent = "".join([
                            i if ord(i) < 128 else ' '
                            for i in wikipage.content
                        ])
                        wikicontent = re.sub(r'\([^)]*\)', '', wikicontent)
                        userin.define_and_execute(
                            ["sensible-browser", wikipage.url], search_query)
                        userin.say(wikicontent)
                    except requests.exceptions.ConnectionError:
                        userin.define_and_execute(
                            [" "], "Wikipedia connection error.")
                        userin.say(
                            "Sorry, " + user_prefix +
                            ". But I'm unable to connect to Wikipedia servers."
                        )
                    except wikipedia.exceptions.DisambiguationError as disambiguation:
                        USER_ANSWERING['status'] = True
                        USER_ANSWERING['for'] = 'wikipedia'
                        USER_ANSWERING['reason'] = 'disambiguation'
                        USER_ANSWERING['options'] = disambiguation.options[:3]
                        notify = "Wikipedia disambiguation. Which one of these you meant?:\n - " + \
                            disambiguation.options[0]
                        message = user_prefix + ", there is a disambiguation. Which one of these you meant? " + \
                            disambiguation.options[0]
                        for option in disambiguation.options[1:3]:
                            message += ", or " + option
                            notify += "\n - " + option
                        notify += '\nSay, for example: "THE FIRST ONE" to choose.'
                        userin.define_and_execute([" "], notify)
                        userin.say(message)
                    except BaseException:
                        pass
        elif "YOUTUBE" in com and ("SEARCH" in com or "FIND" in com):
            tts_kill()
            with nostdout():
                with nostderr():
                    capture = re.search(
                        "(?:SEARCH|FIND) (?P<query>.*) (?:IN|ON|AT|USING)? YOUTUBE", com)
                    if capture:
                        search_query = capture.group('query')
                        info = youtube_dl.YoutubeDL({}).extract_info(
                            'ytsearch:' + search_query,
                            download=False,
                            ie_key='YoutubeSearch')
                        if len(info['entries']) > 0:
                            youtube_title = info['entries'][0]['title']
                            youtube_url = "https://www.youtube.com/watch?v=%s" % (
                                info['entries'][0]['id'])
                            userin.define(["sensible-browser", youtube_url],
                                          youtube_title)
                            youtube_title = "".join([
                                i if ord(i) < 128 else ' '
                                for i in youtube_title
                            ])
                        else:
                            youtube_title = "No video found, " + user_prefix + "."
                            userin.define(" ", " ")
                        userin.execute(0)
                        userin.say(youtube_title)
                        time.sleep(5)
                        k = PyKeyboard()
                        k.tap_key(k.tab_key)
                        k.tap_key(k.tab_key)
                        k.tap_key(k.tab_key)
                        k.tap_key(k.tab_key)
                        k.tap_key('f')
        elif ("GOOGLE" in com
              or "WEB" in com) and "IMAGE" not in com and ("SEARCH" in com
                                                           or "FIND" in com):
            tts_kill()
            with nostdout():
                with nostderr():
                    capture = re.search(
                        "(?:SEARCH|FIND) (?P<query>.*) (?:IN|ON|AT|USING)? (?:GOOGLE|WEB)?", com)
                    if capture:
                        search_query = capture.group('query')
                        tab_url = "http://google.com/?#q=" + search_query
                        userin.define_and_execute(
                            ["sensible-browser", tab_url], search_query)
                        userin.say(search_query)
        elif ("GOOGLE" in com
              or "WEB" in com) and "IMAGE" in com and ("SEARCH" in com
                                                       or "FIND" in com):
            tts_kill()
            with nostdout():
                with nostderr():
                    capture = re.search("(?:SEARCH IMAGES OF|FIND IMAGES OF|SEARCH|FIND) "
                                        "(?P<query>.*) (?:IN|ON|AT|USING)? "
                                        "(?:GOOGLE|WEB|GOOGLE IMAGES|WEB IMAGES)?", com)
                    if capture:
                        search_query = capture.group('query')
                        tab_url = "http://google.com/?#q=" + search_query + "&tbm=isch"
                        userin.define(["sensible-browser", tab_url],
                                      search_query)
                        userin.execute(0)
                        userin.say(search_query)
        else:
            tts_kill()
            learn_response = learn_.respond(com)
            if learn_response:
                userin.define([" "], " ")
                userin.say(learn_response)
            else:
                omniscient_.respond(original_com, not args["silent"], userin,
                                    user_prefix)


def tts_kill():
    subprocess.call(["pkill", "flite"], stdout=FNULL, stderr=FNULL)


def dragon_greet():
    tts_kill()
    print("_______________________________________________________________\n")
    time = datetime.datetime.now().time()

    global user_full_name
    global user_prefix
    global config_file

    command = "getent passwd $LOGNAME | cut -d: -f5 | cut -d, -f1"
    user_full_name = os.popen(command).read()
    user_full_name = user_full_name[:-1]#.decode("utf8")
    home = expanduser("~")
    config_file = TinyDB(home + '/.dragonfire_config.json')
    callme_config = config_file.search(Query().datatype == 'callme')
    if callme_config:
        user_prefix = callme_config[0]['title'].encode("utf8")
    else:
        gender_config = config_file.search(Query().datatype == 'gender')
        if gender_config:
            user_prefix = GENDER_PREFIX[gender_config[0]['gender']]
        else:
            gender = Classifiers.gender(user_full_name.split(' ', 1)[0])
            config_file.insert({'datatype': 'gender', 'gender': gender})
            user_prefix = GENDER_PREFIX[gender]

    if time < datetime.time(12):
        time_of_day = "morning"
    elif datetime.time(12) < time < datetime.time(18):
        time_of_day = "afternoon"
    else:
        time_of_day = "evening"
    userin.define_and_execute(["echo"],
                              "To activate say 'Dragonfire!' or 'Wake Up!'")
    userin.say(" ".join(["Good", time_of_day, user_prefix]))


def speech_error():
    tts_kill()
    userin.define_and_execute(["echo"], "An error occurred")
    userin.say("I couldn't understand, please repeat again")


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
    help_msg = ("Command-line interface mode. Give commands to Dragonfire via command-line inputs (keyboard)"
                "instead of audio inputs (microphone).")
    ap.add_argument("-c", "--cli", help=help_msg, action="store_true")
    help_msg = "Silent mode. Disable Text-to-Speech output. Dragonfire won't generate any audio output."
    ap.add_argument("-s", "--silent", help=help_msg, action="store_true")
    help_msg = "Headless mode. Do not display an avatar animation on the screen. Disable the female head model."
    ap.add_argument("--headless", help=help_msg, action="store_true")
    args = vars(ap.parse_args())
    global userin
    userin = TTA(args)
    try:
        global inactive
        inactive = True
        SystemTrayExitListenerSet(e)
        stray_proc = Process(target=SystemTrayInit)
        stray_proc.start()
        dragon_greet()
        start(args)
    except KeyboardInterrupt:
        stray_proc.terminate()
        sys.exit(1)


if __name__ == '__main__':
    initiate()
