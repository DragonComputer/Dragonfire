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
		self.grammar_model = collections.OrderedDict()
		self.grammar_model = {
			"(?P<col1>.*) (?P<col2>IS|ARE|WAS|WERE|WILL BE) (?P<col3>.*)": "(?:WHO|WHERE|WHEN|WHY|WHAT|WHICH|HOW)(?:.*)(?P<col2>IS|ARE|WAS|WERE|WILL BE) (?P<col1>.*)",
			"(?P<col1>.*) (?P<col2>MEANS?|HAS|HAVE|LIVES?) (?P<col3>.*)": "(?:WHO|WHERE|WHEN|WHY|WHAT|WHICH|HOW)(?:.*)(?:DOES|DO) (?P<col1>.*) (?P<col2>MEAN|HAVE|LIVE)",
			"(?P<col1>.*) (?P<col2>SAID) (?P<col3>.*)": "(?:WHO|WHERE|WHEN|WHY|WHAT|WHICH|HOW)(?:.*)(?:DID) (?P<col1>.*) (?P<col2>SAY)"
		}

	def respond(self,com):
		for statement,question in self.grammar_model.iteritems():

			capture = re.search(question, com)
			if capture:
				answer = capture.group()
				return answer.upper()

			capture = re.search(statement, com)
			if capture:
				#print capture.group('col2')
				#print capture.group('col3')
				#print capture.group('col1')
				answer = capture.group()
				answer = answer.upper()
				for key,value in self.replacements.iteritems():
					if key in answer:
						answer = answer.replace(key,value)
						break
				return "OK, I GET IT. " + answer

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
