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

class WikipediaAnsweringMachine():

	@staticmethod
	def answer(speech, user_prefix):
		#tokens = nltk.word_tokenize(speech)
		#tagged = nltk.pos_tag(tokens)
		topic_obj = TopicExtractor(speech)
		result = topic_obj.extract()
		if "BORN" in speech or "BIRTHDATE" in speech or "DATE " in speech or " DATE" in speech or "WHEN" in speech:
			with nostdout():
				with nostderr():
					try:
						wikipage = wikipedia.page(wikipedia.suggest(result[0]))
						wikicontent = "".join([i if ord(i) < 128 else ' ' for i in wikipage.content])
						wikicontent = re.sub(r'\([^)]*\)', '', wikicontent)
						return TimeDetector.tag(wikicontent)[0]
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
