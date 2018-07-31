#!/usr/bin/python3
# -*- coding: utf-8 -*-

import inspect
import os
import subprocess
import time
from multiprocessing import Pool
from sys import stdout
from random import randint

import realhud

import contextlib  # Utilities for with-statement contexts
try:
    import cStringIO  # Read and write strings as files
except ImportError:
    import io as cStringIO  # Read and write strings as files
import sys  # System-specific parameters and functions

from tweepy.error import TweepError
import metadata_parser
import urllib.request
import mimetypes
import uuid
import shutil

DRAGONFIRE_PATH = os.path.dirname(
    os.path.abspath(inspect.getfile(inspect.currentframe())))
FNULL = open(os.devnull, 'w')
TWITTER_CHAR_LIMIT = 280

songRunning = False


class TextToAction:
    def __init__(self, args):
        self.headless = args["headless"]
        self.silent = args["silent"]
        self.server = args["server"]
        if self.server:
            self.headless = True
            self.silent = True
        self.twitter_api = None
        self.twitter_user = None
        if not self.headless:
            realhud.load_gif(DRAGONFIRE_PATH + "/realhud/animation/avatar.gif")

    def execute(self, cmd="", msg="", speak=False, duration=0):
        self.speak = speak

        if self.server:
            return True
        if self.speak == True:
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

    def say(self, message, dynamic=False, end=False, cmd=None):
        if self.server:
            text = "@" + self.twitter_user + " " + message#.upper()
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
                                if randint(1,3) == 1:
                                    self.twitter_api.create_friendship(self.twitter_user, follow=True)
                            except TweepError as e:
                                print("Warning: " + e.response.text)
                            finally:
                                os.remove(filename)
                            return True
            try:
                self.twitter_api.update_status(text)
                if randint(1,10) == 1:
                    self.twitter_api.create_friendship(self.twitter_user, follow=True)
            except TweepError as e:
                print("Warning: " + e.response.text)
            return True
        # if songRunning == True:
        #   subprocess.Popen(["rhythmbox-client","--pause"])
        if len(message) < 10000:
            (columns, lines) = shutil.get_terminal_size()
            if dynamic:
                if end:
                    print(message.upper())
                    print(columns * "_" + "\n")
                else:
                    print("Dragonfire: " + message.upper(), end=' ')
                    stdout.flush()
            else:
                print("Dragonfire: " + message.upper())
                print(columns * "_" + "\n")
        if not self.silent:
            subprocess.call(["pkill", "flite"], stdout=FNULL, stderr=FNULL)
            tts_proc = subprocess.Popen(
                "flite -voice slt -f /dev/stdin",
                stdin=subprocess.PIPE,
                stdout=FNULL,
                stderr=FNULL,
                shell=True)
            message = "".join([i if ord(i) < 128 else ' ' for i in message])
            tts_proc.stdin.write(message.encode())
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

    def espeak(self, message):
        subprocess.Popen(["espeak", "-v", "en-uk-north", message])


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


if __name__ == "__main__":
    userin = TextToAction()
    userin.say("Hello world!")
