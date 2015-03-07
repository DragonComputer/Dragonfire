#!/usr/bin/python
import subprocess
songRunning = False
class Data:
	def __init__(self, com="", msg="", sp="False"):
		self.command = com
		self.message = msg
		self.speak = sp
	def interact(self):
		if self.command != "":
			subprocess.Popen(self.command,stdout=subprocess.PIPE)
		if self.speak == True:
			self.say(self.message)
		else:
			subprocess.Popen(["notify-send","SoundSight", self.message])
	def say(self,message):
		if songRunning == True:
			subprocess.Popen(["rhythmbox-client","--pause"])
		proc = subprocess.Popen(["festival","--tts"],stdin=subprocess.PIPE)
		proc.stdin.write(message)
		proc.stdin.close()
		proc.wait()
		if songRunning == True:
			subprocess.Popen(["rhythmbox-client","--play"])
