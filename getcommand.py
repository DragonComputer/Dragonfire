#!/usr/bin/python
import sys
import api
from lxml import etree
from api import Data
from subprocess import call


def command(speech_object):
	while(True):
		
		line = speech_object.readline()
		if(line.startswith("sentence1: ")):
			com = line[15:-6]
			print com
        		if(com == "OPEN FILE MANAGER"):
				userin = Data(["pantheon-files"],"Opening files")
	    			userin.interact()
            
			
			

if __name__ == '__main__':
	try:
		command(sys.stdin)
	except KeyboardInterrupt:
		sys.exit(1)
