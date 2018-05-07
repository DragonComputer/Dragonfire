#!/usr/bin/python
# -*- coding: utf-8 -*-

from __future__ import absolute_import, print_function

import inspect
import os
import subprocess
import time
from multiprocessing import Pool
from sys import stdout
from random import randint

import realhud

from tweepy.error import TweepError
import metadata_parser
import urllib.request
import mimetypes
import uuid

DRAGONFIRE_PATH = os.path.dirname(
    os.path.abspath(inspect.getfile(inspect.currentframe())))
FNULL = open(os.devnull, 'w')
TWITTER_CHAR_LIMIT = 280

songRunning = False


class TTA:
    def __init__(self, args):
        self.command = None
        self.message = None

        self.headless = args["headless"]
        self.silent = args["silent"]
        self.twitter = args["twitter"]
        if self.twitter:
            self.headless = True
            self.silent = True
        self.twitter_api = None
        self.twitter_user = None
        realhud.load_gif(DRAGONFIRE_PATH + "/realhud/animation/avatar.gif")

    def define(self, com="", msg="", sp="False"):
        self.command = com
        self.message = msg
        self.speak = sp

    def execute(self, duration):
        if self.twitter:
            return True
        try:
            subprocess.Popen(["notify-send", "Dragonfire", self.message])
        except BaseException:
            pass
        if self.command != "":
            time.sleep(duration)
            try:
                subprocess.Popen(self.command, stdout=FNULL, stderr=FNULL)
            except BaseException:
                pass
        # if self.speak == True:
        #   self.say(self.message)
        # else:

    def define_and_execute(self, com="", msg="", sp="False", duration=0):
        self.command = com
        self.message = msg
        self.speak = sp
        if self.twitter:
            return True
        try:
            subprocess.Popen(["notify-send", "Dragonfire", self.message])
        except BaseException:
            pass
        if self.command != "":
            time.sleep(duration)
            try:
                subprocess.Popen(self.command, stdout=FNULL, stderr=FNULL)
            except BaseException:
                pass

    def say(self, message, dynamic=False, end=False):
        if self.twitter:
            text = "@" + self.twitter_user + " " + message#.upper()
            text = (text[:TWITTER_CHAR_LIMIT]) if len(text) > TWITTER_CHAR_LIMIT else text
            if self.command:
                if len(self.command) > 1:
                    if self.command[0] == "sensible-browser":
                        reduction = len(text + " " + self.command[1]) - TWITTER_CHAR_LIMIT
                        if reduction < 1:
                            reduction = None
                        text = text[:reduction] + " " + self.command[1]
                        page = metadata_parser.MetadataParser(url=self.command[1])
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
            if dynamic:
                if end:
                    print(message.upper())
                    print(
                        "_______________________________________________________________\n"
                    )
                else:
                    print("Dragonfire: " + message.upper(), end=' ')
                    stdout.flush()
            else:
                print("Dragonfire: " + message.upper())
                print(
                    "_______________________________________________________________\n"
                )
        if not self.silent:
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


if __name__ == "__main__":
    userin = TTA()
    userin.define([" "], " ")
    userin.say("Hello world!")
