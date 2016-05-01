#!/usr/bin/python
# -*- coding: utf-8 -*-

import nltk
import wikipedia
from dragonfire.nlplib import TopicExtractor
from dragonfire.timex import TimeDetector
import sys
import contextlib
import cStringIO
import re
from random import randint
from nltk.tag import SennaNERTagger
from collections import Counter

class WikipediaAnsweringMachine():

	@staticmethod
	def answer(speech, user_prefix):
		#tokens = nltk.word_tokenize(speech)
		#tagged = nltk.pos_tag(tokens)
		topic_obj = TopicExtractor(speech)
		result = topic_obj.extract()
		try:
			print "~Topic: " + result[0]
		except:
			pass
		speech = speech.upper()
		if "WHEN" in speech or "BIRTHDATE" in speech or "DATE " in speech or " DATE" in speech or "BORN" in speech:
			with nostdout():
				with nostderr():
					try:
						wikipage = wikipedia.page(result[0])
						wikicontent = "".join([i if ord(i) < 128 else ' ' for i in wikipage.content])
						#print TimeDetector.tag(wikicontent)
						count = Counter(TimeDetector.tag(wikicontent))
						return count.most_common()[0][0]
					except:
						return noanswer(user_prefix)
		elif "WHERE" in speech or "LOCATION" in speech or "ADDRESS" in speech or "COUNTRY" in speech or "CITY" in speech or "STREET" in speech:
			with nostdout():
				with nostderr():
					try:
						wikipage = wikipedia.page(result[0])
						wikicontent = "".join([i if ord(i) < 128 else ' ' for i in wikipage.content])
						wikicontent = re.sub(r'\([^)]*\)', '', wikicontent)
						nertagger = SennaNERTagger('/usr/share/senna')
						tagged = nertagger.tag(wikicontent.split())
						for tag in tagged:
							if tag[1] == 'B-LOC':
								return tag[0]
						return noanswer(user_prefix)
					except:
						return noanswer(user_prefix)
		else:
			with nostdout():
				with nostderr():
					try:
						summary = wikipedia.summary(result[0], sentences=1)
						summary = "".join([i if ord(i) < 128 else ' ' for i in summary])
						summary = re.sub(r'\([^)]*\)', '', summary)
						return summary
					except:
						return noanswer(user_prefix)

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
	print WikipediaAnsweringMachine.answer("At eight o'clock on Thursday morning Arthur didn't feel very good.")
