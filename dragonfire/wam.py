#!/usr/bin/python
# -*- coding: utf-8 -*-

import nltk
import wikipedia
from dragonfire.nlplib import TopicExtractor
import sys
import contextlib
import cStringIO
import re

class WikipediaAnsweringMachine():

	@staticmethod
	def answer(speech):
		#tokens = nltk.word_tokenize(speech)
		#tagged = nltk.pos_tag(tokens)
		topic_obj = TopicExtractor(speech)
		result = topic_obj.extract()
		with nostdout():
			with nostderr():
				summary = wikipedia.summary(result[0], sentences=1)
				summary = "".join([i if ord(i) < 128 else ' ' for i in summary])
				summary = re.sub(r'\([^)]*\)', '', summary)
		return summary

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
