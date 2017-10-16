from random import randint # Random integer generator
import collections # Imported to support ordered dictionaries in Python
import re # Regular expression operations library of Python
from tinydb import TinyDB, Query # TinyDB is a lightweight document oriented database
from os.path import expanduser # Imported to get the home directory
import spacy # Most powerful NLP library available - spaCy

class Learn():

	def __init__(self):
		self.replacements = collections.OrderedDict() # Create an ordered dictionary
		self.replacements["I'M"] = "YOU ARE"
		self.replacements["I WAS"] = "YOU WERE"
		self.replacements["I "] = "YOU "
		self.replacements["MY"] = "YOUR"
		self.replacements["MYSELF"] = "YOURSELF"
		home = expanduser("~") # Get the home directory of the user
		self.db = TinyDB(home + '/.dragonfire_db.json') # This is where we store the database; /home/USERNAME/.dragonfire_db.json
		self.nlp = spacy.load('en') # Load en_core_web_sm, English, 50 MB, default model

	# Entry function for this class. Dragonfire calls only this function. It does not handle TTS.
	def respond(self,com):
		forget = "^(?:FORGET|UPDATE) (?:EVERYTHING YOU KNOW ABOUT |ABOUT )?(?P<subject>.*)"
		capture = re.search(forget, com)
		if capture:
			if self.db.remove(Query().subject == self.pronoun_fixer(capture.group('subject'))): # if there is a record about the subject in the database then remove that record and...
				return "OK, I FORGOT EVERYTHING I KNOW ABOUT " + self.mirror(capture.group('subject'))
			else:
				return "I WASN'T EVEN KNOW ANYTHING ABOUT " + self.mirror(capture.group('subject'))

		define = "(?:PLEASE )?(?:DEFINE|EXPLAIN|TELL ME ABOUT|DESCRIBE) (?P<subject>.*)" # TODO: Extend the context of this regular expression
		capture = re.search(define, com)
		result = None
		if capture:
			return self.db_getter(capture.group('subject'))

		doc = self.nlp(com.decode('utf-8')) # Command(user's speech) must be decoded from utf-8 to unicode because spaCy only supports unicode strings, self.nlp() handles all parsing
		subject = [] # subject list (subjects here usually are; I'M, YOU, HE, SHE, IT, etc.)
		prev_type = None # type of the previous noun phrase
		for np in doc.noun_chunks: # Iterate over the noun phrases(chunks) TODO: Cover 'dobj' also; doc = nlp(u'DESCRIBE THE SUN') >>> (u'THE SUN', u'SUN', u'dobj', u'DESCRIBE')
			# Purpose of this if statement is completing possessive form of nouns
			if np.root.dep_ == 'pobj' and prev_type == 'nsubj': # if it's an object of a preposition and the previous noun phrase's type was nsubj(nominal subject) then (it's purpose is capturing subject like MY PLACE OF BIRTH)
				subject.append(np.root.head.text.encode('utf-8')) # append the parent text from syntactic relations tree (example: while nsubj is 'MY PLACE', np.root.head.text is 'OF')
				subject.append(np.text.encode('utf-8')) # append the text of this noun phrase (example: while nsubj is 'MY PLACE', np.text is 'BIRTH')
			prev_type = None # make it None on each iteration after it completes its mission
			if np.root.dep_ == 'nsubj' and np.root.tag_ != 'WP': # if it's a nsubj(nominal subject). "wh-" words are also considered as nsubj(nominal subject) but they are out of scope. This is why we are excluding them.
				subject.append(np.text.encode('utf-8')) # append the text of this noun phrase
				prev_type = 'nsubj' # assign the previous type as nsubj(nominal subject)
		subject = ' '.join(subject).strip() # concatenate all noun phrases found
		if subject: # if the subject is not empty
			wh_found = False
			for word in doc: # iterate over the each word in the given command(user's speech)
				if word.tag_ in ['WDT','WP','WP$','WRB']: # check if there is a "wh-" question (we are determining that if it's a question or not, so only accepting questions with "wh-" form)
					wh_found = True
			if wh_found: # if that's a question
				return self.db_getter(subject) # return the answer from the database
			else:
				verb_found = False
				verbtense = None # verbtense is the am/is/are of the main sentence
				clause = [] # is the information that we need to acknowledge
				for word in doc:
					if verb_found: # get the all words comes after the first verb which will be our verbtense
						clause.append(word.text.encode('utf-8'))
					if word.pos_ == 'VERB' and not verb_found: # if that's a verb and verb does not found yet then
						verb_found = True # verb is found
						verbtense = word.text.encode('utf-8') # append it to verbtense
				clause = ' '.join(clause).strip() # concatenate the clause
				return(self.db_setter(subject,verbtense,clause,com)) # set the record to the database

	# Function to get a record from the database
	def db_getter(self,subject):
		result = self.db.search(Query().subject == subject) # make a database search by giving subject string
		if result: # if there is a result
			dictionary = {}
			for row in result: # iterate over the rows of the result
				if row['verbtense'] not in dictionary: # if the verbtense is not in the keys of the dictionary
					dictionary[row['verbtense']] = [] # then add it
				if row['clause'] not in dictionary[row['verbtense']]: # if the clause is not in the value like; dictionary['is']
					dictionary[row['verbtense']].append(row['clause']) # then append the clause
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
	def db_setter(self,subject,verbtense,clause,com):
		if not self.db.search( (Query().subject == subject) & (Query().verbtense == verbtense) & (Query().clause == clause) ): # if there is no exacty record on the database then
			self.db.insert({'subject': subject, 'verbtense': verbtense, 'clause': clause}) # insert the given data
		return "OK, I GET IT. " + self.mirror(com) # mirror the command(user's speech) and return it to say

	# Function to mirror the answer (for example: I'M to YOU ARE)
	def mirror(self,answer):
		answer = answer.upper() # make the given string fully uppercase
		for key,value in self.replacements.iteritems(): # iterate over the replacements
			if key in answer: # if the key is in the answer
				return answer.replace(key,value) # replace and return
		for value,key in self.replacements.iteritems(): # invert the process above
			if key in answer:
				return answer.replace(key,value)
		return answer # return the same string if there is no replacement

	# Pronoun fixer to handle situations like YOU and YOURSELF
	def pronoun_fixer(self,subject): # TODO: Extend the context of this function
		subject = subject.upper()
		if 'YOURSELF' in subject:
			subject = subject.replace('YOURSELF','YOU')
		return subject


if __name__ == "__main__":
	learn_ = Learn()
	print learn_.respond("THE SUN IS HOT")
	print learn_.respond("THE SUN IS YELLOW")
	print learn_.respond("WHAT IS THE SUN")

	print learn_.respond("YOU ARE JUST A COMPUTER PROGRAM")
	print learn_.respond("WHAT ARE YOU")
	print learn_.respond("FORGET EVERYTHING YOU KNOW ABOUT YOURSELF")
