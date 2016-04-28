#!/usr/bin/python
# -*- coding: utf-8 -*-

import nltk
import wikipedia

class WikipediaAnsweringMachine():

	@staticmethod
	def answer(speech):
		tokens = nltk.word_tokenize(speech)
		tagged = nltk.pos_tag(tokens)
		print tagged

if __name__ == "__main__":
	WikipediaAnsweringMachine.answer("At eight o'clock on Thursday morning Arthur didn't feel very good.")
