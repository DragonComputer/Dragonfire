#!/usr/bin/python
# -*- coding: utf-8 -*-
import sys
import api
from lxml import etree
from api import Data
from subprocess import call
import time
import subprocess
import urllib2
import wikipedia
from random import randint
import getpass
import os
import ConfigParser
import xml.etree.ElementTree as ET
from pykeyboard import PyKeyboard
import datetime
from apiclient.discovery import build
from apiclient.errors import HttpError
import glob

def command(speech_object):
	previous_command = ""
	global inactive
	while(True):
		
		line = speech_object.readline()
		if(line.startswith("sentence1: ")):
			com = line[15:-6]
			if (inactive == 1 and com != "DRAGON FIRE" and com != "WAKEUP"):
				continue
			print com

                	Config = ConfigParser.ConfigParser()
                	Config.read("config.ini")
                	user_prefix = Config.get("BasicUserData","Prefix")

			if (com == "DRAGON FIRE" or com == "WAKEUP"):
				tts_kill()
				inactive = 0
				userin = Data([" "]," ")
				words_dragonfire = {
					0 : "Yes, " + user_prefix + ".",
					1 : "Yes. I'm waiting.",
					2 : "What is your orders?"
				}
				userin.say(words_dragonfire[randint(0,2)])
			elif (com == "GO TO SLEEP"):
				tts_kill()
				inactive = 1
                                userin = Data(["echo"],"Dragonfire deactivated. To reactivate say 'Dragonfire!' or 'Wake Up!'")
                                userin.say("I'm going to sleep")
                                userin.interact(0)
                                previous_command = com
			elif (com == "ENOUGH" or com == "OKAY"):
				tts_kill()
			elif (com == "WHO AM I" or com == "WHAT IS MY NAME"):
                                tts_kill()
				user_full_name = os.popen("getent passwd $LOGNAME | cut -d: -f5 | cut -d, -f1").read()
				user_full_name = user_full_name[:-1]
                                userin = Data(["echo"], user_full_name)
                                userin.say("Your name is " + user_full_name + "," + user_prefix + ".")
				userin.interact(0)
                                previous_command = com
			elif (com == "I'M A WOMAN" or com == "I'M A GIRL" or com == "I'M A LADY"):
				tts_kill()
				cfgfile = open("config.ini",'w')
				Config.set("BasicUserData","Prefix","My Lady")
				Config.write(cfgfile)
				cfgfile.close()
				userin = Data([" "]," ")
				userin.say("Pardon, My Lady.")
                        elif (com == "I'M A MAN" or com == "I'M A BOY"):
                                tts_kill()
                                cfgfile = open("config.ini",'w')
                                Config.set("BasicUserData","Prefix","Sir")
                                Config.write(cfgfile)
                                cfgfile.close()
                                userin = Data([" "]," ")
                                userin.say("Pardon, Sir.")
			elif (com == "WHAT IS YOUR NAME"):
				tts_kill()
				userin = Data([" "]," ")
				userin.say("My name is Dragon Fire.")
				previous_command = com
			elif (com == "WHAT IS YOUR GENDER"):
				tts_kill()
                                userin = Data([" "]," ")
                                userin.say("I have a female voice but I don't have a gender identity. I'm a computer program, " + user_prefix + ".")
                                previous_command = com
        		elif (com == "OPEN FILE MANAGER"):
				tts_kill()
				userin = Data(["pantheon-files"],"File Manager")
				userin.say("File Manager")
				userin.interact(0)
				previous_command = com
			elif (com == "OPEN WEB BROWSER"):
				tts_kill()
				userin = Data(["sensible-browser"],"Web Browser")
				userin.say("Web Browser")
				userin.interact(0)
				previous_command = com
			elif (com == "SHUT DOWN THE COMPUTER"):
				tts_kill()
                                userin = Data(["sudo","poweroff"],"Shutting down")
                                userin.say("Shutting down")
				userin.interact(3)
                                previous_command = com
			elif (com.startswith("WIKI PEDIA SEARCH FOR")):
				tts_kill()
				userin = Data(["sensible-browser","http://en.wikipedia.org/wiki/"+com[22:].lower()],com[22:])
				userin.interact(0)
				try:
					wikipage = wikipedia.page(com[22:].lower())
					wikicontent = "".join([i if ord(i) < 128 else ' ' for i in wikipage.content])
					userin.say(wikicontent)
            				previous_command = com
				except:
					pass
			elif (com.startswith("YOU TUBE SEARCH FOR")):
				tts_kill()

				DEVELOPER_KEY = "AIzaSyAcwHj2qzI7KWDUN4RkBTX8Y4lrU78lncA"
				YOUTUBE_API_SERVICE_NAME = "youtube"
				YOUTUBE_API_VERSION = "v3"

				youtube = build(YOUTUBE_API_SERVICE_NAME, YOUTUBE_API_VERSION, developerKey=DEVELOPER_KEY)

				search_response = youtube.search().list(q=com[20:].lower().replace(" ", "%20"), part="id,snippet").execute()

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

				#print "Videos:\n", "\n".join(videos), "\n"
				#print "Channels:\n", "\n".join(channels), "\n"
				#print "Playlists:\n", "\n".join(playlists), "\n"

				youtube_title = videos[0]
				youtube_url = "https://www.youtube.com/watch?v=%s" % (videos[1])

				#root = ET.fromstring(urllib2.urlopen("http://gdata.youtube.com/feeds/api/videos?vq=" + com[20:].lower().replace(" ", "%20") + "&racy=include&orderby=relevance&start-index=1&max-results=1").read())
				
				#for child in root[15]:
				#	if child.tag == "{http://www.w3.org/2005/Atom}title":
				#		youtube_title = child.text
				#	if child.tag == "{http://www.w3.org/2005/Atom}link":
				#		youtube_url = child.attrib["href"]
				#		break				

				userin = Data(["sensible-browser",youtube_url],youtube_title)
				youtube_title = "".join([i if ord(i) < 128 else ' ' for i in youtube_title])
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
                                userin = Data(["echo"],com + " ?")
                                userin.say("Unrecognized command.")
                                userin.interact(0)
                                previous_command = com
			newest = max(glob.iglob('./audio_recordings/*.[Ww][Aa][Vv]'), key=os.path.getctime)
			print newest
			os.system('rm ./audio_recordings/*')


def tts_kill():
	call(["pkill", "audsp"])
	call(["pkill", "aplay"])

def dragon_greet():
	time = datetime.datetime.now().time()

	Config = ConfigParser.ConfigParser()
        Config.read("config.ini")
        user_prefix = Config.get("BasicUserData","Prefix")
	
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

if __name__ == '__main__':
	try:
		inactive = 1
		dragon_greet()
		command(sys.stdin)
	except KeyboardInterrupt:
		sys.exit(1)
