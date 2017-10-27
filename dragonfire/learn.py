from __future__ import print_function
import collections # Imported to support ordered dictionaries in Python
import re # Regular expression operations library of Python
from tinydb import TinyDB, Query # TinyDB is a lightweight document oriented database
from os.path import expanduser # Imported to get the home directory
import spacy # Most powerful NLP library available - spaCy

class Learn():

	def __init__(self):
		self.replacements = collections.OrderedDict() # Create an ordered dictionary
		self.replacements["I'M"] = "YOU-ARE"
		self.replacements["I-WAS"] = "YOU-WERE"
		self.replacements["I"] = "YOU"
		self.replacements["MY"] = "YOUR"
		self.replacements["MINE"] = "YOURS"
		self.replacements["MYSELF"] = "YOURSELF"
		self.replacements["OURSELVES"] = "YOURSELVES"
		home = expanduser("~") # Get the home directory of the user
		self.db = TinyDB(home + '/.dragonfire_db.json') # This is where we store the database; /home/USERNAME/.dragonfire_db.json
		self.nlp = spacy.load('en') # Load en_core_web_sm, English, 50 MB, default model

	# Entry function for this class. Dragonfire calls only this function. It does not handle TTS.
	def respond(self, com):
		forget = "^(?:FORGET|UPDATE) (?:EVERYTHING YOU KNOW ABOUT |ABOUT )?(?P<subject>.*)"
		capture = re.search(forget, com)
		if capture:
			if self.db.remove(Query().subject == self.pronoun_fixer(capture.group('subject'))): # if there is a record about the subject in the database then remove that record and...
				return "OK, I FORGOT EVERYTHING I KNOW ABOUT " + self.mirror(capture.group('subject'))
			else:
				return "I DON'T EVEN KNOW ANYTHING ABOUT " + self.mirror(capture.group('subject'))

		define = "(?:PLEASE |COULD YOU )?(?:DEFINE|EXPLAIN|TELL ME ABOUT|DESCRIBE) (?P<subject>.*)"
		capture = re.search(define, com)
		if capture:
			return self.db_getter(capture.group('subject'))

		doc = self.nlp(com.decode('utf-8')) # Command(user's speech) must be decoded from utf-8 to unicode because spaCy only supports unicode strings, self.nlp() handles all parsing
		subject = [] # subject list (subjects here usually are; I'M, YOU, HE, SHE, IT, etc.)
		prev_type = None # type of the previous noun phrase
		for np in doc.noun_chunks: # Iterate over the noun phrases(chunks) TODO: Cover 'dobj' also; doc = nlp(u'DESCRIBE THE SUN') >>> (u'THE SUN', u'SUN', u'dobj', u'DESCRIBE')
			# Purpose of this if statement is completing possessive form of nouns
			if np.root.dep_ == 'pobj': # if it's an object of a preposition
				if prev_type == 'nsubj': # and the previous noun phrase's type was nsubj(nominal subject) then (it's purpose is capturing subject like MY PLACE OF BIRTH)
					subject.append(np.root.head.text.encode('utf-8')) # append the parent text from syntactic relations tree (example: while nsubj is 'MY PLACE', np.root.head.text is 'OF')
					subject.append(np.text.encode('utf-8')) # append the text of this noun phrase (example: while nsubj is 'MY PLACE', np.text is 'BIRTH')
				prev_type = 'pobj' # assign the previous type as pobj
			if np.root.dep_ == 'nsubj': # if it's a nsubj(nominal subject)
				if np.root.tag_ != 'WP' and prev_type not in ['pobj', 'nsubj']: # "wh-" words are also considered as nsubj(nominal subject) but they are out of scope. This is why we are excluding them.
					subject.append(np.text.encode('utf-8')) # append the text of this noun phrase
				prev_type = 'nsubj' # assign the previous type as nsubj(nominal subject)
				if np.root.tag_ == 'WP':
					prev_type = 'WP'
			if np.root.dep_ == 'attr': # if it's an attribute
				if prev_type not in ['pobj', 'nsubj']: # and the previous noun phrase's type was nsubj(nominal subject)
					subject.append(np.text.encode('utf-8')) # append the text of this noun phrase
				prev_type = 'attr'
		subject = ' '.join(subject).strip() # concatenate all noun phrases found
		if subject: # if the subject is not empty
			wh_found = False
			for word in doc: # iterate over the each word in the given command(user's speech)
				if word.tag_ in ['WDT','WP','WP$','WRB']: # check if there is a "wh-" question (we are determining that if it's a question or not, so only accepting questions with "wh-" form)
					wh_found = True
			if wh_found: # if that's a question
				straight = self.db_getter(subject) # get the answer from the database
				if straight is None:
					return self.db_getter(subject, True) # if nothing found then invert
				return straight
			else:
				verb_found = False
				verbtense = None # verbtense is the am/is/are of the main sentence
				clause = [] # is the information that we need to acknowledge
				for word in doc:
					if verb_found: # get the all words comes after the first verb which will be our verbtense
						if word.pos_ != 'PUNCT': # exclude punctuations
							clause.append(word.text.encode('utf-8'))
					if word.pos_ == 'VERB' and not verb_found: # if that's a verb and verb does not found yet then
						verb_found = True # verb is found
						verbtense = word.text.encode('utf-8') # append it to verbtense
				clause = ' '.join(clause).strip() # concatenate the clause
				return self.db_setter(subject, verbtense, clause, com) # set the record to the database

	# Function to get a record from the database
	def db_getter(self, subject, invert=False):
		if invert:
			result = self.db.search(Query().clause == subject) # make a database search by giving subject string (inverted)
		else:
			result = self.db.search(Query().subject == subject) # make a database search by giving subject string
		if result: # if there is a result
			dictionary = {}
			for row in result: # iterate over the rows of the result
				if row['verbtense'] not in dictionary: # if the verbtense is not in the keys of the dictionary
					dictionary[row['verbtense']] = [] # then add it
				if row['clause'] not in dictionary[row['verbtense']]: # if the clause is not in the value like; dictionary['is']
					dictionary[row['verbtense']].append(row['clause']) # then append the clause
			if invert:
				answer = row['subject'] # in WHO questions subject is actually the clause so we learn the subject from db
			else:
				answer = subject # the answer we will return
			first_verbtense = False
			for key, value in dictionary.iteritems(): # iterate over the dictionary defined and assigned on above
				if not first_verbtense: # if the first verbtense assignment does not made yet
					answer += ' ' + str(key) # concatenate with a whitespace
					first_verbtense = True
				else:
					answer += ', ' + str(key) # otherwise concatenate with a comma + whitespace
				first_clause = False
				for clause in value: # iterate over the clauses of the key
					if not first_clause: # if the first verbtense assignment does not made yet
						answer += ' ' + clause # concatenate with a whitespace
						first_clause = True
					else:
						answer += ' AND ' + clause # otherwise concatenate with ' AND '
			return self.mirror(answer) # mirror the answer (for example: I'M to YOU ARE)
		else:
			return None # if there is no result return None

	# Function to set a record to the database
	def db_setter(self, subject, verbtense, clause, com):
		if not self.db.search( (Query().subject == subject) & (Query().verbtense == verbtense) & (Query().clause == clause) ): # if there is no exacty record on the database then
			self.db.insert({'subject': subject, 'verbtense': verbtense, 'clause': clause}) # insert the given data
		return "OK, I GET IT. " + self.mirror(com) # mirror the command(user's speech) and return it to say

	# Function to mirror the answer (for example: I'M to YOU ARE)
	def mirror(self, answer):
		answer = answer.upper() # make the given string fully uppercase
		answer = self.forward_replace(answer)
		result = []
		for word in answer.split(): # for each word in the answer
			replaced = False
			for key,value in self.replacements.iteritems(): # iterate over the replacements
				if word == key: # if the word is equal to key
					result.append(value) # append the value
					replaced = True
			if word in ["WE","US"]:
				result.append("YOU")
				replaced = True
			elif word == "OUR":
				result.append("YOUR")
				replaced = True
			elif word == "OURS":
				result.append("YOURS")
				replaced = True
			if not replaced:
				result.append(word) # otherwise append the word
		if ' '.join(result) != answer: # if there is a replacement
			return self.backward_replace(' '.join(result)) # return the result
		result = []
		for word in answer.split(): # for each word in the answer
			replaced = False
			for value,key in self.replacements.iteritems(): # invert the process above
				if word == key: # if the word is equal to key
					result.append(value) # append the value
					replaced = True
			if not replaced:
				result.append(word) # otherwise append the word
		return self.backward_replace(' '.join(result)) # return the result anyway

	def forward_replace(self, string):
		string = string.replace("I WAS", "I-WAS")
		string = string.replace("YOU ARE", "YOU-ARE")
		string = string.replace("YOU WERE", "YOU-WERE")
		return string

	def backward_replace(self, string):
		string = string.replace("I-WAS", "I WAS")
		string = string.replace("YOU-ARE", "YOU ARE")
		string = string.replace("YOU-WERE", "YOU WERE")
		return string

	# Pronoun fixer to handle situations like YOU and YOURSELF
	def pronoun_fixer(self, subject): # TODO: Extend the context of this function
		subject = subject.upper()
		if 'YOURSELF' in subject:
			subject = subject.replace('YOURSELF', 'YOU')
		return subject


if __name__ == "__main__":
	import os
	home = expanduser("~") # Get the home directory of the user
	os.remove(home + '/.dragonfire_db.json') # This is where we store the database; /home/USERNAME/.dragonfire_db.json
	learn_ = Learn()

	def give_and_get(give, get):
		result = learn_.respond(give)
		if result != get:
		    print("{} | {}".format(give, result))

	gives_and_gets = collections.OrderedDict()
	gives_and_gets["THE SUN IS HOT"] = "OK, I GET IT. THE SUN IS HOT"
	gives_and_gets["THE SUN IS YELLOW"] = "OK, I GET IT. THE SUN IS YELLOW"
	gives_and_gets["DESCRIBE THE SUN"] = "THE SUN IS HOT AND YELLOW"
	gives_and_gets["WHAT IS THE SUN"] = "THE SUN IS HOT AND YELLOW"
	gives_and_gets["MY AGE IS 25"] = "OK, I GET IT. YOUR AGE IS 25"
	gives_and_gets["WHAT IS MY AGE"] = "YOUR AGE IS 25"
	gives_and_gets["FORGET MY AGE"] = "OK, I FORGOT EVERYTHING I KNOW ABOUT YOUR AGE"
	gives_and_gets["UPDATE MY AGE"] = "I DON'T EVEN KNOW ANYTHING ABOUT YOUR AGE"
	gives_and_gets["MY PLACE OF BIRTH IS TURKEY"] = "OK, I GET IT. YOUR PLACE OF BIRTH IS TURKEY"
	gives_and_gets["WHERE IS MY PLACE OF BIRTH"] = "YOUR PLACE OF BIRTH IS TURKEY"
	gives_and_gets["YOU ARE JUST A COMPUTER PROGRAM"] = "OK, I GET IT. I'M JUST A COMPUTER PROGRAM"
	gives_and_gets["WHAT ARE YOU"] = "I'M JUST A COMPUTER PROGRAM"
	gives_and_gets["FORGET EVERYTHING YOU KNOW ABOUT YOURSELF"] = "OK, I FORGOT EVERYTHING I KNOW ABOUT MYSELF"
	gives_and_gets["MINE IS GOLDEN"] = "OK, I GET IT. YOURS IS GOLDEN"
	gives_and_gets["HOW IS MINE"] = "YOURS IS GOLDEN"
	gives_and_gets["ALBERT EINSTEIN IS A PHYSICIST"] = "OK, I GET IT. ALBERT EINSTEIN IS A PHYSICIST"
	gives_and_gets["WHO IS A PHYSICIST"] = "ALBERT EINSTEIN IS A PHYSICIST"

	for give, get in gives_and_gets.items():
		give_and_get(give, get)
