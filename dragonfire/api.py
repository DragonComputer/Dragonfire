#!/usr/bin/python
import subprocess
import time

songRunning = False
class Data:
	def __init__(self, com="", msg="", sp="False"):
		self.command = com
		self.message = msg
		self.speak = sp
	def interact(self,duration):
		subprocess.Popen(["notify-send","Dragonfire", self.message])
		if self.command != "":
			time.sleep(duration)
			subprocess.Popen(self.command,stdout=subprocess.PIPE)
		#if self.speak == True:
		#	self.say(self.message)
		#else:
	def say(self,message):
		#if songRunning == True:
		#	subprocess.Popen(["rhythmbox-client","--pause"])
		proc = subprocess.Popen(["festival","--tts"],stdin=subprocess.PIPE)
		proc.stdin.write(message)
		proc.stdin.close()
		#proc.wait()
		#if songRunning == True:
		#	subprocess.Popen(["rhythmbox-client","--play"])
	def espeak(self,message):
		subprocess.Popen(["espeak","-v","en-uk-north",message])
