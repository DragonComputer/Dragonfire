#!/usr/bin/python
# -*- coding: utf-8 -*-

import subprocess
import time
import os

FNULL = open(os.devnull, 'w')

songRunning = False
class Data:
	def __init__(self, com="", msg="", sp="False"):
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
	def say(self,message):
		#if songRunning == True:
		#	subprocess.Popen(["rhythmbox-client","--pause"])
		if len(message) < 10000:
			print "Dragonfire: " + message.upper()
		print "_______________________________________________________________\n"
		proc = subprocess.Popen(["festival","--tts"], stdin=subprocess.PIPE, stdout=FNULL, stderr=FNULL)
		message = "".join([i if ord(i) < 128 else ' ' for i in message])
		proc.stdin.write(message)
		proc.stdin.close()
		#proc.wait()
		#if songRunning == True:
		#	subprocess.Popen(["rhythmbox-client","--play"])
	def espeak(self,message):
		subprocess.Popen(["espeak","-v","en-uk-north",message])

if __name__ == "__main__":
	userin = Data([" "]," ")
	userin.say("I have a female voice but I don't have a gender identity. I'm a computer program.")
