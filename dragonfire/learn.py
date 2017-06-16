import json
import urllib
import urllib2
import time
import sys
import contextlib
import cStringIO
from random import randint
import collections
import pkg_resources
import xml.etree.ElementTree as ET
import re

class Aiml():

	def __init__(self):
		self.dictionary = collections.OrderedDict()
		tree = ET.parse(pkg_resources.resource_filename('dragonfire', 'aiml/computers.aiml'))
		root = tree.getroot()
		#print collection.toxml()
		categories = root.findall("category")
		for category in categories:
			key = self.patternParser(category.find("pattern"))
			value = self.templateParser(category.find("template"))
			self.dictionary[key] = value

	def respond(self,com):
		for key,value in self.dictionary.iteritems():
			print key
			matches = re.findall(key, com)
			print matches
			if matches:
				for match in matches:
					print match
				return value

	def patternParser(self,this_node):
	    return this_node.text.replace('*','(.*)')

	def templateParser(self,this_node):
		i = 0
		for child in this_node.iter():
			if child.tag == 'set':
				this_node.remove(child)
				this_node.insert(i, 'asdas')
			i += 1
		return this_node.text


def noanswer(user_prefix):
	words_dragonfire = {
	0 : "I'm not that smart, " + user_prefix + ".",
	1 : "Please, be simple.",
	2 : "Excuse me? I have an average IQ."
	}
	return words_dragonfire[randint(0,2)]

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
	AimlObj = Aiml()
	print AimlObj.respond("MY COMPUTER IS AN ASSHOLE")
