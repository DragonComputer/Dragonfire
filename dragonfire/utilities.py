#!/usr/bin/python
# -*- coding: utf-8 -*-

from sys import stdout
import subprocess
import time
import os
import inspect
import realhud
import sys
import contextlib
import cStringIO
from multiprocessing import Pool

DRAGONFIRE_PATH = os.path.dirname(os.path.abspath(inspect.getfile(inspect.currentframe())))
FNULL = open(os.devnull, 'w')

songRunning = False
class TTA:

	def __init__(self):
		realhud.load_gif(DRAGONFIRE_PATH + "/realhud/animation/avatar.gif")

	def define(self, com="", msg="", sp="False"):
		self.command = com
		self.message = msg
		self.speak = sp

	def interact(self,duration):
		try:
			subprocess.Popen(["notify-send","Dragonfire", self.message])
		except:
			pass
		if self.command != "":
			time.sleep(duration)
			try:
				subprocess.Popen(self.command, stdout=FNULL, stderr=FNULL)
			except:
				pass
		#if self.speak == True:
		#	self.say(self.message)
		#else:

	def say(self,message,dynamic=False,end=False):
		#if songRunning == True:
		#	subprocess.Popen(["rhythmbox-client","--pause"])
		if len(message) < 10000:
			if dynamic:
				if end:
					print message.upper()
					print "_______________________________________________________________\n"
				else:
					print "Dragonfire: " + message.upper(),
					stdout.flush()
			else:
				print "Dragonfire: " + message.upper()
				print "_______________________________________________________________\n"
		tts_proc = subprocess.Popen("festival --tts", stdin=subprocess.PIPE, stdout=FNULL, stderr=FNULL, shell=True)
		message = "".join([i if ord(i) < 128 else ' ' for i in message])
		tts_proc.stdin.write(message)
		tts_proc.stdin.close()
		#print "TTS process started."

		pool = Pool(processes=1)
		pool.apply_async(realhud.play_gif, [0.5, True])
		#print "Avatar process started."

		tts_proc.wait()
		pool.terminate()
		#if songRunning == True:
		#	subprocess.Popen(["rhythmbox-client","--play"])

	def espeak(self,message):
		subprocess.Popen(["espeak","-v","en-uk-north",message])

	def play_gif_wrapper(opacity,is_click_through):
		with nostdout():
			with nostderr():
				realhud.play_gif(opacity, is_click_through)


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
	userin = TTA()
	userin.define([" "]," ")
	userin.say("Hello world!")
