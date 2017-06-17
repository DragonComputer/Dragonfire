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
		self.replacements = {"I'M": "YOU", "YOU ARE": "I'M", "YOU": "I'M", "MY ": "YOUR ", "YOUR ": "MY "}
		self.dictionary = collections.OrderedDict()
		root = etree.parse(pkg_resources.resource_filename('dragonfire', 'aiml/dragonfire.aiml'))
		categories = root.findall("category")
		for category in categories:
			statement = category.find("statement").text
			question = category.find("question").text
			self.dictionary[statement] = question

	def respond(self,com):
		for statement,question in self.dictionary.iteritems():
			result = []

			matches = re.findall(question, com)
			if matches:
				for match in matches[0]:
					result.append(match)
				return ' '.join(result).upper()

			matches = re.findall(statement, com)
			if matches:
				for match in matches[0]:
					result.append(match)
				result = ' '.join(result).upper()
				for key,value in self.replacements.iteritems():
					if key in result:
						result = result.replace(key,value)
						break
				return "OK, I GET IT. " + result

		return None


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
	print AimlObj.respond("MY AGE IS 24")
