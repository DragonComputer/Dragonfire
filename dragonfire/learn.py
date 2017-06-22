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
import spacy

class Learn():

	def __init__(self):
		self.replacements = collections.OrderedDict()
		self.replacements["I'M"] = "YOU ARE"
		self.replacements["I WAS"] = "YOU WERE"
		self.replacements["I "] = "YOU "
		self.replacements["MY"] = "YOUR"
		home = expanduser("~")
		self.db = TinyDB(home + '/.dragonfire_db.json')
		self.nlp = spacy.load('en')

	def respond(self,com):
		forget = "^(?:FORGET|UPDATE) (?:ABOUT )?(?P<subject>.*)"
		capture = re.search(forget, com)
		if capture:
			if self.db.remove(Query().subject == capture.group('subject')):
				return "OK, I FORGOT EVERYTHING I KNOW ABOUT " + self.mirror(capture.group('subject').upper())
			else:
				return "I WASN'T EVEN KNOW ANYTHING ABOUT " + self.mirror(capture.group('subject').upper())

		define = "(?:PLEASE )?(?:DEFINE|EXPLAIN|TELL ME ABOUT|DESCRIBE) (?P<subject>.*)"
		capture = re.search(define, com)
		result = None
		if capture:
			return self.db_getter(capture.group('subject'))

		doc = self.nlp(com.decode('utf-8'))
		subject = []
		prev_type = None
		for np in doc.noun_chunks:
			if np.root.dep_ == 'pobj' and prev_type == 'nsubj':
				subject.append(np.root.head.text.encode('utf-8'))
				subject.append(np.text.encode('utf-8'))
			prev_type = None
			if np.root.dep_ == 'nsubj' and np.root.tag_ != 'WP':
				subject.append(np.text.encode('utf-8'))
				prev_type = 'nsubj'
		subject = ' '.join(subject).strip()
		if subject:
			wh_found = False
			for word in doc:
				if word.tag_ in ['WDT','WP','WP$','WRB']:
					wh_found = True
			if wh_found:
				return self.db_getter(subject)
			else:
				verb_found = False
				verbtense = None
				clause = []
				for word in doc:
					if verb_found:
						clause.append(word.text.encode('utf-8'))
					if word.pos_ == 'VERB' and not verb_found:
						verb_found = True
						verbtense = word.text.encode('utf-8')
				clause = ' '.join(clause).strip()
				return(self.db_setter(subject,verbtense,clause,com))

	def db_getter(self,subject):
		result = self.db.search(Query().subject == subject)
		if result:
			dictionary = {}
			for row in result:
				if row['verbtense'] not in dictionary:
					dictionary[row['verbtense']] = []
				if row['clause'] not in dictionary[row['verbtense']]:
					dictionary[row['verbtense']].append(row['clause'])
			answer = subject
			first_verbtense = False
			for key, value in dictionary.iteritems():
				if not first_verbtense:
					answer += ' ' + key
					first_verbtense = True
				else:
					answer += ', ' + key
				first_clause = False
				for clause in value:
					if not first_clause:
						answer += ' ' + clause
						first_clause = True
					else:
						answer += ' AND ' + clause
			return self.mirror(answer)
		else:
			return None

	def db_setter(self,subject,verbtense,clause,com):
		if not self.db.search( (Query().subject == subject) & (Query().verbtense == verbtense) & (Query().clause == clause) ):
			self.db.insert({'subject': subject, 'verbtense': verbtense, 'clause': clause})
		return "OK, I GET IT. " + self.mirror(com)

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
