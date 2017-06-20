import sys
import contextlib
import cStringIO
from random import randint
import collections
import pkg_resources
from lxml import etree
import re
from tinydb import TinyDB, Query
from os.path import expanduser

class Aiml():

	def __init__(self):
		self.replacements = collections.OrderedDict()
		self.replacements["I'M"] = "YOU ARE"
		self.replacements["I WAS"] = "YOU WERE"
		self.replacements["I "] = "YOU "
		self.replacements["MY"] = "YOUR"
		self.grammar_model = collections.OrderedDict()
		self.grammar_model["(?P<subject>.*) (?P<verbtense>IS|ARE|WAS|WERE|WILL BE) (?P<clause>.*)"] = "(?:WHO|WHERE|WHEN|WHY|WHAT|WHICH|HOW)(?:.*)(?P<verbtense>IS|ARE|WAS|WERE|WILL BE) (?P<subject>.*)"
		self.grammar_model["(?P<subject>.*) (?P<verbtense>MEANS?|HAS|HAVE|LIVES?) (?P<clause>.*)"] = "(?:WHO|WHERE|WHEN|WHY|WHAT|WHICH|HOW)(?:.*)(?:DOES|DO) (?P<subject>.*) (?P<verbtense>MEAN|HAVE|LIVE)"
		self.grammar_model["(?P<subject>.*) (?P<verbtense>SAID) (?P<clause>.*)"] = "(?:WHO|WHERE|WHEN|WHY|WHAT|WHICH|HOW)(?:.*)(?:DID) (?P<subject>.*) (?P<verbtense>SAY)"
		self.grammar_model["\b\B"] = "(?:DEFINE|EXPLAIN|TELL ME ABOUT|DESCRIBE) (?P<subject>.*)"
		home = expanduser("~")
		self.db = TinyDB(home + '/.dragonfire_db.json')

	def respond(self,com):
		forget = "^(?:FORGET|UPDATE) (?:ABOUT )?(?P<subject>.*)"
		capture = re.search(forget, com)
		if capture:
			if self.db.remove(Query().subject == capture.group('subject')):
				return "OK, I FORGOT EVERYTHING I KNOW ABOUT " + capture.group('subject').upper()
			else:
				return "I WASN'T EVEN KNOW ANYTHING ABOUT " + capture.group('subject').upper()

		for statement,question in self.grammar_model.iteritems():

			capture = re.search(question, com)
			if capture:
				result = self.db.search(Query().subject == capture.group('subject'))
				if result:
					for row in result:
						original_clause = row['clause']
						for item in result[:]:
							if row['verbtense'] == item['verbtense'] and original_clause != item['clause']:
								row['clause'] = row['clause'] + ' AND ' + item['clause']
								result.remove(item)
					answer = ''
					for row in result:
						if answer:
							answer += ', '
						answer += row['subject'] + ' ' + row['verbtense'] + ' ' + row['clause']
					return self.mirror(answer)
				else:
					return None

			capture = re.search(statement, com)
			if capture:
				if not self.db.search( (Query().subject == capture.group('subject')) & (Query().verbtense == capture.group('verbtense')) & (Query().clause == capture.group('clause')) ):
					self.db.insert({'subject': capture.group('subject'), 'verbtense': capture.group('verbtense'), 'clause': capture.group('clause')})
				answer = self.mirror(capture.group())
				return "OK, I GET IT. " + answer

		return None

	def mirror(self,answer):
		answer = answer.upper()
		for key,value in self.replacements.iteritems():
			if key in answer:
				answer = answer.replace(key,value)
				return answer
		for value,key in self.replacements.iteritems():
			if key in answer:
				answer = answer.replace(key,value)
				return answer
		return answer

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
	print AimlObj.respond("THE SUN IS HOT")
	print AimlObj.respond("THE SUN IS YELLOW")
	print AimlObj.respond("WHAT IS THE SUN")
