#!/usr/bin/python
# -*- coding: utf-8 -*-

import sys
from lxml import etree
from dragonfire.utilities import Data
from dragonfire.nlplib import Classifiers
from dragonfire.yoda import YodaQA
from subprocess import call, Popen
import time
import subprocess
import urllib2
import wikipedia
from random import randint
import getpass
import os
import re
import xml.etree.ElementTree as ET
from pykeyboard import PyKeyboard
from pymouse import PyMouse
import datetime
from apiclient.discovery import build
from apiclient.errors import HttpError
import glob
import speech_recognition as sr
import inspect
#import aiml
import contextlib
import cStringIO
from dragonfire.learn import Aiml
import uuid
import string

DRAGONFIRE_PATH = os.path.dirname(os.path.abspath(inspect.getfile(inspect.currentframe())))
FNULL = open(os.devnull, 'w')
GENDER_PREFIX = {'male': 'Sir', 'female': 'My Lady'}
CONVO_ID = uuid.uuid4()
LEARN = Aiml()

def command(speech):
	#here = os.path.dirname(os.path.realpath(__file__))
	#os.chdir(os.path.expanduser("~/yodaqa/"))
	#Popen(["./gradlew","web","-q"], stdout=FNULL, stderr=FNULL)
	#os.chdir(here)

	'''
	kernel = aiml.Kernel()
	with nostdout():
		with nostderr():
			kernel.learn(DRAGONFIRE_PATH + "/aiml/learn.aiml")
	'''

	previous_command = ""
	global inactive

	global user_full_name
	global user_prefix

	while(True):

		line = speech.readline()
		if line.startswith("sentence1: ") or line.startswith("<search failed>"):
			com = google_speech_api()
			if com == "\n" or com == " ":
				com = "Enter"
			original_com = com

			if (com == 0):
				#speech_error()
				continue

			com = com.upper()
			print "You: " + com

			if inactive == 1 and "DRAGONFIRE" != com and "DRAGON FIRE" != com and "WAKE UP" != com and com != "HEY":
				continue

			if "DRAGONFIRE" == com or "DRAGON FIRE" == com or "WAKE UP" == com or com == "HEY":
				tts_kill()
				inactive = 0
				userin = Data([" "]," ")
				words_dragonfire = {
					0 : "Yes, " + user_prefix + ".",
					1 : "Yes. I'm waiting.",
					2 : "What is your orders?"
				}
				userin.say(words_dragonfire[randint(0,2)])
			elif "GO TO SLEEP" == com:
				tts_kill()
				inactive = 1
				userin = Data(["echo"],"Dragonfire deactivated. To reactivate say 'Dragonfire!' or 'Wake Up!'")
				userin.say("I'm going to sleep")
				userin.interact(0)
				previous_command = com
			elif "ENOUGH" == com or "SHUT UP" == com:
				print "Dragonfire quiets."
				tts_kill()
			elif "WHO AM I" == com or "SAY MY NAME" == com:
				tts_kill()
				userin = Data(["echo"], user_full_name)
				userin.say("Your name is " + user_full_name + ", " + user_prefix + ".")
				userin.interact(0)
				previous_command = com
			elif "MY TITLE IS LADY" == com or "I'M A LADY" == com or "I'M A WOMAN" == com or "I'M A GIRL" == com:
				tts_kill()
				user_prefix = "My Lady"
				userin = Data([" "]," ")
				userin.say("Pardon, " + user_prefix + ".")
			elif "MY TITLE IS SIR" == com or "I'M A MAN" == com or "I'M A BOY" == com:
				tts_kill()
				user_prefix = "Sir"
				userin = Data([" "]," ")
				userin.say("Pardon, " + user_prefix + ".")
			elif "WHAT IS YOUR NAME" == com:
				tts_kill()
				userin = Data([" "],"My name is Dragonfire.")
				userin.say("My name is Dragon Fire.")
				userin.interact(0)
				previous_command = com
			elif "WHAT IS YOUR GENDER" == com:
				tts_kill()
				userin = Data([" "]," ")
				userin.say("I have a female voice but I don't have a gender identity. I'm a computer program, " + user_prefix + ".")
				previous_command = com
			elif "FILE MANAGER" in com or "OPEN FILES" == com:
				tts_kill()
				userin = Data(["dolphin"],"File Manager") # KDE neon
				userin.interact(0)
				userin = Data(["pantheon-files"],"File Manager") # elementary OS
				userin.interact(0)
				userin = Data(["nautilus","--browser"],"File Manager") # Ubuntu
				userin.say("File Manager")
				userin.interact(0)
				previous_command = com
			elif "WEB BROWSER" in com:
				tts_kill()
				userin = Data(["sensible-browser"],"Web Browser")
				userin.say("Web Browser")
				userin.interact(0)
				previous_command = com
			elif "OPEN BLENDER" == com:
				tts_kill()
				userin = Data(["blender"],"Blender")
				userin.say("Blender 3D computer graphics software")
				userin.interact(0)
				previous_command = com
			elif "PHOTO SHOP" in com or "PHOTO EDITOR" in com or "GIMP" in com:
				tts_kill()
				userin = Data(["gimp"],"GIMP")
				userin.say("Photo editor")
				userin.interact(0)
				previous_command = com
			elif "INKSCAPE" in com or "VECTOR GRAPHICS" in com or "VECTORIAL DRAWING" in com:
				tts_kill()
				userin = Data(["inkscape"],"Inkscape")
				userin.say("Inkscape")
				userin.interact(0)
				previous_command = com
			elif "VIDEO EDITOR" in com:
				tts_kill()
				#userin = Data(["openshot"],"Openshot")
				#userin.interact(0)
				#userin = Data(["lightworks"],"Lightworks")
				#userin.interact(0)
				userin = Data(["kdenlive"],"Kdenlive")
				userin.say("Video editor")
				userin.interact(0)
				previous_command = com
			elif "OPEN CAMERA" == com:
				tts_kill()
				userin = Data(["kamoso"],"Camera") # KDE neon
				userin.interact(0)
				userin = Data(["snap-photobooth"],"Camera") # elementary OS
				userin.interact(0)
				userin = Data(["cheese"],"Camera") # Ubuntu
				userin.say("Camera")
				userin.interact(0)
				previous_command = com
			elif "OPEN CALENDAR" == com:
				tts_kill()
				userin = Data(["korganizer"],"Calendar") # KDE neon
				userin.interact(0)
				userin = Data(["maya-calendar"],"Calendar") # elementary OS
				userin.interact(0)
				userin = Data(["orage"],"Calendar") # Ubuntu
				userin.say("Calendar")
				userin.interact(0)
				previous_command = com
			elif "OPEN CALCULATOR" == com:
				tts_kill()
				userin = Data(["kcalc"],"Calculator") # KDE neon
				userin.interact(0)
				userin = Data(["pantheon-calculator"],"Calculator") # elementary OS
				userin.interact(0)
				userin = Data(["gnome-calculator"],"Calculator") # Ubuntu
				userin.say("Calculator")
				userin.interact(0)
				previous_command = com
			elif "OPEN STEAM" == com:
				tts_kill()
				userin = Data(["steam"],"Steam")
				userin.say("Steam Game Store")
				userin.interact(0)
				previous_command = com
			elif "SOFTWARE CENTER" in com:
				tts_kill()
				userin = Data(["plasma-discover"],"Software Center") # KDE neon
				userin.interact(0)
				userin = Data(["software-center"],"Software Center") # elementary OS & Ubuntu
				userin.say("Software Center")
				userin.interact(0)
				previous_command = com
			elif "OFFICE SUITE" in com:
				tts_kill()
				userin = Data(["libreoffice"],"LibreOffice")
				userin.say("Office Suite")
				userin.interact(0)
				previous_command = com
			elif "OPEN WRITER" == com:
				tts_kill()
				userin = Data(["libreoffice","--writer"],"LibreOffice Writer")
				userin.say("Writer")
				userin.interact(0)
				previous_command = com
			elif "OPEN MATH" == com:
				tts_kill()
				userin = Data(["libreoffice","--math"],"LibreOffice Math")
				userin.say("Math")
				userin.interact(0)
				previous_command = com
			elif "OPEN IMPRESS" == com:
				tts_kill()
				userin = Data(["libreoffice","--impress"],"LibreOffice Impress")
				userin.say("Impress")
				userin.interact(0)
				previous_command = com
			elif "OPEN DRAW" == com:
				tts_kill()
				userin = Data(["libreoffice","--draw"],"LibreOffice Draw")
				userin.say("Draw")
				userin.interact(0)
				previous_command = com
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
						k.press_keys([k.control_l_key,'t'])
			elif com == "SWITCH TAB":
				tts_kill()
				with nostdout():
					with nostderr():
						k = PyKeyboard()
						k.press_keys([k.control_l_key,k.tab_key])
			elif com == "CLOSE" or com == "ESCAPE":
				tts_kill()
				with nostdout():
					with nostderr():
						k = PyKeyboard()
						k.press_keys([k.control_l_key,'w'])
						k.tap_key(k.escape_key)
			elif com == "GO BACK":
				tts_kill()
				with nostdout():
					with nostderr():
						k = PyKeyboard()
						k.press_keys([k.alt_l_key,k.left_key])
			elif com == "GO FORWARD":
				tts_kill()
				with nostdout():
					with nostderr():
						k = PyKeyboard()
						k.press_keys([k.alt_l_key,k.right_key])
			elif com == "SCROLL LEFT":
				tts_kill()
				with nostdout():
					with nostderr():
						m = PyMouse()
						m.scroll(0,-5)
			elif com == "SCROLL RIGHT":
				tts_kill()
				with nostdout():
					with nostderr():
						m = PyMouse()
						m.scroll(0,5)
			elif com == "SCROLL UP":
				tts_kill()
				with nostdout():
					with nostderr():
						m = PyMouse()
						m.scroll(5,0)
			elif com == "SCROLL DOWN":
				tts_kill()
				with nostdout():
					with nostderr():
						m = PyMouse()
						m.scroll(-5,0)
			elif com == "PLAY" or com == "PAUSE" or com == "SPACEBAR":
				tts_kill()
				with nostdout():
					with nostderr():
						k = PyKeyboard()
						k.tap_key(" ")
			elif "SHUTDOWN THE COMPUTER" == com:
				tts_kill()
				userin = Data(["sudo","poweroff"],"Shutting down")
				userin.say("Shutting down")
				userin.interact(3)
				previous_command = com
			elif com == "GOODBYE" or com == "BYE BYE" or com == "SEE YOU LATER":
				tts_kill()
				userin = Data([" "]," ")
				userin.say("Goodbye, " + user_prefix)
				previous_command = com
				julius_proc.terminate()
				with nostdout():
					with nostderr():
						try:
							os.system('rm /tmp/' + str(datetime.date.today().year) + '*.[Ww][Aa][Vv]')
						except:
							pass
				sys.exit(1)
			elif "WIKIPEDIA" in com and ("SEARCH" in com or "FIND" in com):
				tts_kill()
				wikicontent = ""
				with nostdout():
					with nostderr():
						capture = re.search("(?:SEARCH|FIND) (?P<query>.*) (?:IN|ON|AT|USING)? WIKIPEDIA", com)
						if capture:
							search_query = capture.group('query')

							userin = Data(["sensible-browser","http://en.wikipedia.org/wiki/"+search_query.lower()],search_query)
							userin.interact(0)
							try:
								wikipage = wikipedia.page(search_query)
								wikicontent = "".join([i if ord(i) < 128 else ' ' for i in wikipage.content])
								wikicontent = re.sub(r'\([^)]*\)', '', wikicontent)
							except:
								pass
				userin.say(wikicontent)
				previous_command = com
			elif "YOUTUBE" in com and "SEARCH" in com:
				tts_kill()
				with nostdout():
					with nostderr():
						search_query = com.replace("SEARCH ", "").replace(" SEARCH", "").replace(" IN YOUTUBE", "").replace("IN YOUTUBE ", "").replace(" ON YOUTUBE", "").replace("ON YOUTUBE ", "").replace(" USING YOUTUBE", "").replace("USING YOUTUBE ", "").replace(" YOUTUBE", "").replace("YOUTUBE ", "")

						DEVELOPER_KEY = "AIzaSyAcwHj2qzI7KWDUN4RkBTX8Y4lrU78lncA"
						YOUTUBE_API_SERVICE_NAME = "youtube"
						YOUTUBE_API_VERSION = "v3"

						youtube = build(YOUTUBE_API_SERVICE_NAME, YOUTUBE_API_VERSION, developerKey=DEVELOPER_KEY)

						search_response = youtube.search().list(q=search_query, part="id,snippet", maxResults=1).execute()

						videos = []
						channels = []
						playlists = []

						# Add each result to the appropriate list, and then display the lists of
						# matching videos, channels, and playlists.
						for search_result in search_response.get("items", []):
							if search_result["id"]["kind"] == "youtube#video":
								  #videos.append("%s (%s)" % (search_result["snippet"]["title"], search_result["id"]["videoId"]))
								videos.append(search_result["snippet"]["title"])
								videos.append(search_result["id"]["videoId"])
							elif search_result["id"]["kind"] == "youtube#channel":
								channels.append("%s (%s)" % (search_result["snippet"]["title"], search_result["id"]["channelId"]))
							elif search_result["id"]["kind"] == "youtube#playlist":
								playlists.append("%s (%s)" % (search_result["snippet"]["title"], search_result["id"]["playlistId"]))

						if len(videos) > 1:
							youtube_title = videos[0]
							youtube_url = "https://www.youtube.com/watch?v=%s" % (videos[1])
							userin = Data(["sensible-browser",youtube_url],youtube_title)
							youtube_title = "".join([i if ord(i) < 128 else ' ' for i in youtube_title])
						else:
							youtube_title = "No video found, " + user_prefix + "."
							userin = Data("",youtube_title)
						k = PyKeyboard()
						k.tap_key('space')
				userin.say(youtube_title)
				userin.interact(0)
				time.sleep(3)
				k.tap_key(k.tab_key)
				k.tap_key(k.tab_key)
				k.tap_key(k.tab_key)
				k.tap_key(k.tab_key)
				k.tap_key('f')
			else:
				tts_kill()
				#dragonfire_respond = kernel.respond(com)
				aiml_respond = LEARN.respond(com)
				if aiml_respond:
					userin = Data([" "]," ")
					userin.say(aiml_respond)
				#if aiml_respond and "WHAT" not in aiml_respond and "WHERE" not in aiml_respond and "WHO" not in aiml_respond and "WHEN" not in aiml_respond and "WHICH" not in aiml_respond and "HOW" not in aiml_respond:
				#	userin.say(aiml_respond)
				#else:
				#	userin.say("I need to do a brief research on the internet. It may take up to 3 minutes, so please be patient.")
				#	userin.say(YodaQA.answer("http://qa.ailao.eu", original_com, user_prefix))
				previous_command = com

			#newest = max(glob.iglob('/tmp/' + str(datetime.date.today().year) + '*.[Ww][Aa][Vv]'), key=os.path.getctime)
			#print newest


def tts_kill():
	call(["pkill", "audsp"], stdout=FNULL, stderr=FNULL)
	call(["pkill", "aplay"], stdout=FNULL, stderr=FNULL)

def dragon_greet():
	tts_kill()
	print "_______________________________________________________________\n"
	time = datetime.datetime.now().time()

	global user_full_name
	global user_prefix

	user_full_name = os.popen("getent passwd $LOGNAME | cut -d: -f5 | cut -d, -f1").read()
	user_full_name = user_full_name[:-1]
	user_prefix = GENDER_PREFIX[Classifiers.gender(user_full_name.split(' ', 1)[0])]

	if time < datetime.time(12):
		userin = Data(["echo"],"To activate say 'Dragonfire!' or 'Wake Up!'")
		userin.say("Good morning " + user_prefix)
		userin.interact(0)
	elif datetime.time(12) < time  and time < datetime.time(18):
		userin = Data(["echo"],"To activate say 'Dragonfire!' or 'Wake Up!'")
		userin.say("Good afternoon " + user_prefix)
		userin.interact(0)
	else:
		userin = Data(["echo"],"To activate say 'Dragonfire!' or 'Wake Up!'")
		userin.say("Good evening " + user_prefix)
		userin.interact(0)

def google_speech_api():

	newest_recording = max(glob.iglob('/tmp/' + str(datetime.date.today().year) + '*.[Ww][Aa][Vv]'), key=os.path.getctime)

	r = sr.Recognizer()
	with sr.WavFile(newest_recording) as source:            # use "test.wav" as the audio source
		audio = r.record(source)                        # extract audio data from the file
	try:
		return r.recognize_google(audio)   # recognize speech using Google Speech Recognition
	except:
		pass
	return 0

def speech_error():
	tts_kill()
	userin = Data(["echo"],"An error occurred")
	userin.say("I couldn't understand, please repeat again")
	userin.interact(0)

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
	try:
		global inactive
		global julius_proc
		inactive = 1
		dragon_greet()
		# padsp julius -input mic -C julian.jconf | ./getcommand.py
		julius_proc = subprocess.Popen(["padsp", "julius", "-input", "mic", "-C", DRAGONFIRE_PATH + "/julian.jconf"], stdout=subprocess.PIPE, stderr=subprocess.PIPE)
		speech = julius_proc.stdout
		command(speech)
		#command(sys.stdin)
	except:
		julius_proc.terminate()
		with nostdout():
			with nostderr():
				try:
					os.system('rm /tmp/' + str(datetime.date.today().year) + '*.[Ww][Aa][Vv]')
				except:
					pass
		sys.exit(1)

if __name__ == '__main__':
	try:
		inactive = 1
		dragon_greet()
		# padsp julius -input mic -C julian.jconf | ./getcommand.py
		sys.stdin = subprocess.Popen(["padsp", "julius", "-input", "mic", "-C", DRAGONFIRE_PATH + "julian.jconf"], stdout=subprocess.PIPE).stdout
		command(sys.stdin)
	except:
		sys.exit(1)
