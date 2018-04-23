#!/usr/bin/python
# -*- coding: utf-8 -*-

from __future__ import absolute_import, print_function

import inspect
import os
import subprocess
import time
from multiprocessing import Pool
from sys import stdout

import realhud

DRAGONFIRE_PATH = os.path.dirname(
    os.path.abspath(inspect.getfile(inspect.currentframe())))
FNULL = open(os.devnull, 'w')

songRunning = False


class TTA:
    def __init__(self, args):
        self.headless = args["headless"]
        self.silent = args["silent"]
        realhud.load_gif(DRAGONFIRE_PATH + "/realhud/animation/avatar.gif")

    def define(self, com="", msg="", sp="False"):
        self.command = com
        self.message = msg
        self.speak = sp

    def execute(self, duration):
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
