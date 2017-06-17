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
from lxml import etree
import re

class Aiml():

	def __init__(self):
		self.dictionary = collections.OrderedDict()
		root = etree.parse(pkg_resources.resource_filename('dragonfire', 'aiml/computers.aiml'))
		categories = root.findall("category")
		for category in categories:
			key = self.patternParser(category)
			value = self.templateParser(category)
			self.dictionary[key] = value

	def respond(self,com):
		for key,value in self.dictionary.iteritems():
			print key
			matches = re.findall(key, com)
			if matches:
				i = 1
				for match in matches:
					value = value.replace('$'+str(i), match)
					i += 1
				return value.upper()

	def patternParser(self,category):
		return category.find("pattern").text.replace('*','(.*)')

	def templateParser(self,category):
		i = 1
		for child in category.find("template").iterchildren():
			if child.tag == 'set':
				child.text = '$' + str(i)
				i += 1

		etree.strip_tags(category.find("template"),'set')
		return category.find("template").text


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
