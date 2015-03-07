#!/usr/bin/python
import sys
import api
from lxml import etree
from api import Data
from subprocess import call
import time


def command(speech_object):
	previous_command = ""
	while(True):
		line = speech_object.readline()
		if(line.startswith("sentence1: ")):
			com = line[15:-6]
			if (previous_command == com):
				continue
			print com
			if (com == "DRAGON FIRE"):
				userin = Data([" "]," ")
				userin.espeak("Yes sir")
				previous_command = com
			if (com == "WHAT IS YOUR NAME"):
				userin = Data([" "]," ")
				userin.espeak("My name is Dragonfire.")
				previous_command = com
        		if(com == "OPEN FILE MANAGER"):
				userin = Data(["pantheon-files"],"File Manager")
	    			userin.interact()
				userin.espeak("File Manager")
				previous_command = com
			if(com == "OPEN WEB BROWSER"):
				userin= Data(["sensible-browser"],"Web Browser")
				userin.interact()
				userin.espeak("Web Browser")
				previous_command = com
            
			
			

if __name__ == '__main__':
	try:
		command(sys.stdin)
	except KeyboardInterrupt:
		sys.exit(1)
