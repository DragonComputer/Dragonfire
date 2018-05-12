from __future__ import print_function
import collections  # Imported to support ordered dictionaries in Python
from tinydb import TinyDB, Query # TinyDB is a lightweight document oriented database
from os.path import expanduser  # Imported to get the home directory


class Learn():
    def __init__(self, nlp):
        self.pronouns = collections.OrderedDict()  # Create an ordered dictionary
        self.pronouns["I"] = "YOU"
        self.pronouns["ME"] = "YOU"
        self.pronouns["MY"] = "YOUR"
        self.pronouns["MINE"] = "YOURS"
        self.pronouns["MYSELF"] = "YOURSELF"
        self.pronouns["OUR"] = "YOUR"
        self.pronouns["OURS"] = "YOURS"
        self.pronouns["OURSELVES"] = "YOURSELVES"
        self.pronouns["WE"] = "YOU"
        self.pronouns["US"] = "YOU"
        self.inv_pronouns = collections.OrderedDict()  # Create an ordered dictionary
        self.inv_pronouns["YOU"] = "I"
        self.inv_pronouns["YOUR"] = "MY"
        self.inv_pronouns["YOURS"] = "MINE"
        self.inv_pronouns["YOURSELF"] = "MYSELF"
        self.inv_pronouns["YOURSELVES"] = "OURSELVES"

        self.auxiliaries = collections.OrderedDict()  # Create an ordered dictionary
        self.auxiliaries["AM"] = "ARE"
        self.auxiliaries["'M"] = " ARE"
        self.auxiliaries["WAS"] = "WERE"
        self.inv_auxiliaries = collections.OrderedDict()  # Create an ordered dictionary
        self.inv_auxiliaries["ARE"] = "AM"
        self.inv_auxiliaries["WERE"] = "WAS"

        home = expanduser("~")  # Get the home directory of the user
        self.db = TinyDB(home + '/.dragonfire_db.json') # This is where we store the database; /home/USERNAME/.dragonfire_db.json
        self.nlp = nlp  # Load en_core_web_sm, English, 50 MB, default model

    # Entry function for this class. Dragonfire calls only this function. It does not handle TTS.
    def respond(self, com):
        doc = self.nlp(com) # Command(user's speech) must be decoded from utf-8 to unicode because spaCy only supports unicode strings, self.nlp() handles all parsing
        subject = [] # subject list (subjects here usually are; I'M, YOU, HE, SHE, IT, etc.)
        types = [] # types of the previous noun phrases
        types.append("")
        for np in doc.noun_chunks: # Iterate over the noun phrases(chunks) TODO: Cover 'dobj' also; doc = nlp(u'DESCRIBE THE SUN') >>> (u'THE SUN', u'SUN', u'dobj', u'DESCRIBE')
            types.append(np.root.dep_)
            # Purpose of this if statement is completing possessive form of nouns
            if np.root.dep_ == 'pobj' and types[-2] == 'nsubj':  # if it's an object of a preposition and the previous noun phrase's type was nsubj(nominal subject) then (it's purpose is capturing subject like MY PLACE OF BIRTH)
                subject.append(np.root.head.text) # append the parent text from syntactic relations tree (example: while nsubj is 'MY PLACE', np.root.head.text is 'OF')
                subject.append(np.text) # append the text of this noun phrase (example: while nsubj is 'MY PLACE', np.text is 'BIRTH')
            if np.root.dep_ == 'nsubj' and types[-2] not in ['pobj', 'nsubj'] and np.root.tag_ not in ['WDT', 'WP', 'WP$', 'WRB']:  # if it's a nsubj(nominal subject) ("wh-" words can be considered as nsubj(nominal subject) but they are out of scope.  This is why we are excluding them.)
                subject.append(np.text)  # append the text of this noun phrase
            if np.root.dep_ == 'attr' and types[-2] not in ['pobj', 'nsubj'] and np.root.tag_ not in ['WDT', 'WP', 'WP$', 'WRB']: # if it's an attribute and the previous noun phrase's type was not nsubj(nominal subject)
                subject.append(np.text)  # append the text of this noun phrase
            if np.root.dep_ == 'dobj' and types[-2] not in ['pobj', 'nsubj'] and np.root.tag_ not in ['WDT', 'WP', 'WP$', 'WRB']:  # if it's a dobj(direct object) and the previous noun phrase's type was not nsubj(nominal subject)
                subject.append(np.text)  # append the text of this noun phrase
        subject = [x for x in subject]
        subject = ' '.join(subject).strip() # concatenate all noun phrases found
        if subject: # if the subject is not empty
            wh_found = False
            for word in doc: # iterate over the each word in the given command(user's speech)
                if word.tag_ in ['WDT', 'WP', 'WP$', 'WRB']: # check if there is a "wh-" question (we are determining that if it's a question or not, so only accepting questions with "wh-" form)
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
                verbs = []
                for word in doc:
                    #print(word.text, word.lemma_, word.pos_, word.tag_, word.dep_, word.shape_, word.is_alpha, word.is_stop)
                    if verb_found: # get the all words comes after the first verb which will be our verbtense
                        if word.pos_ != 'PUNCT': # exclude punctuations
                            clause.append(word.text)
                    if word.pos_ == 'VERB' and word.is_stop and not verb_found: # if that's a verb and verb does not found yet then
                        verb_found = True # verb is found
                        verbtense = word.text # append it to verbtense
                    if word.pos_ == 'VERB':
                        verbs.append(word.text)
                clause = [x for x in clause]
                clause = ' '.join(clause).strip() # concatenate the clause

                # keywords to order get and remove operations on the database
                if any(verb in verbs for verb in self.capitalizer(["forget", "remove", "delete", "update"])):
                    if self.db.remove(Query().subject == self.pronoun_fixer(subject)): # if there is a record about the subject in the database then remove that record and...
                        return "OK, I forgot everything I know about " + self.mirror(subject)
                    else:
                        return "I don't even know anything about " + self.mirror(subject)

                if any(verb in verbs for verb in self.capitalizer(["define", "explain", "tell", "describe"])):
                    return self.db_getter(subject)

                if verbtense:
                    return self.db_setter(subject, verbtense, clause,com)  # set the record to the database

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
            for key, value in dictionary.items(): # iterate over the dictionary defined and assigned on above
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
                        answer += ' and ' + clause # otherwise concatenate with ' AND '
            return self.mirror(answer) # mirror the answer (for example: I'M to YOU ARE)
        else:
            return None # if there is no result return None

    # Function to set a record to the database
    def db_setter(self, subject, verbtense, clause, com):
        if not self.db.search(
            (Query().subject == subject) & (Query().verbtense == verbtense) & (Query().clause == clause)
        ): # if there is no exacty record on the database then
            self.db.insert({
                'subject': subject,
                'verbtense': verbtense,
                'clause': clause
            }) # insert the given data
        return "OK, I get it. " + self.mirror(com) # mirror the command(user's speech) and return it to say

    # Function to mirror the answer (for example: I'M to YOU ARE)
    def mirror(self, answer):
        result = []
        types = []
        types.append("")
        doc = self.nlp(answer)
        for token in doc:
            types.append(token.lemma_)
            if token.lemma_ == "-PRON-": # if it's a pronoun, mirror it
                if token.text.upper() in self.pronouns:
                    result.append(self.pronouns[token.text.upper()].lower())
                    continue
                if token.text.upper() in self.inv_pronouns:
                    result.append(self.inv_pronouns[token.text.upper()].lower())
                    continue
            if (token.lemma_ == "be" or token.dep_ == "aux") and types[-2] == "-PRON-": # if it's an auxiliary that comes right after a pronoun, mirror it
                if token.text.upper() in self.auxiliaries:
                    result.append(self.auxiliaries[token.text.upper()].lower())
                    continue
                if token.text.upper() in self.inv_auxiliaries:
                    result.append(self.inv_auxiliaries[token.text.upper()].lower())
                    continue
            result.append(token.text)
        for i in range(len(result)):
            if result[i] == "i":
                result[i] = "I"
        result = ' '.join(result) # concatenate the result
        result = result.replace(" '", "'") # fix for situations like "I 'AM", "YOU 'LL"
        return result

    # Pronoun fixer to handle situations like YOU and YOURSELF
    def pronoun_fixer(self, subject):  # TODO: Extend the context of this function
        if subject == "yourself":
            return "you"
        elif subject == "Yourself":
            return "You"
        elif subject == "YOURSELF":
            return "YOU"
        else:
            return subject

    def capitalizer(self, array):
        result = []
        for word in array:
            result.append(word)
            result.append(word.capitalize())
            result.append(word.upper())
        return result


if __name__ == "__main__":
    # TESTS
    import os
    import spacy
    home = expanduser("~") # Get the home directory of the user
    if os.path.exists(home + '/.dragonfire_db.json'):
        os.remove(home + '/.dragonfire_db.json') # This is where we store the database; /home/USERNAME/.dragonfire_db.json
    learn_ = Learn(spacy.load('en'))

    def give_and_get(give, get):
        result = learn_.respond(give)
        if not result:
            print("{} | {}".format(give, result))
            return False
        if result != get:
            print("{} | {}".format(give, result))
            return False
        return True

    gives_and_gets = collections.OrderedDict()
    gives_and_gets["the Sun is hot"] = "OK, I get it. the Sun is hot"
    gives_and_gets["the Sun is yellow"] = "OK, I get it. the Sun is yellow"
    gives_and_gets["Describe the Sun"] = "the Sun is hot and yellow"
    gives_and_gets["What is the Sun"] = "the Sun is hot and yellow"
    gives_and_gets["my age is 25"] = "OK, I get it. your age is 25"
    gives_and_gets["What is my age"] = "your age is 25"
    gives_and_gets["forget my age"] = "OK, I forgot everything I know about your age"
    gives_and_gets["update my age"] = "I don't even know anything about your age"
    gives_and_gets["my place of birth is Turkey"] = "OK, I get it. your place of birth is Turkey"
    gives_and_gets["Where is my place of birth"] = "your place of birth is Turkey"
    gives_and_gets["you are just a computer program"] = "OK, I get it. I am just a computer program"
    gives_and_gets["What are you"] = "I am just a computer program"
    gives_and_gets["mine is golden"] = "OK, I get it. yours is golden"
    gives_and_gets["how is mine"] = "yours is golden"
    gives_and_gets["Albert Einstein is a Physicist"] = "OK, I get it. Albert Einstein is a Physicist"
    gives_and_gets["Who is a Physicist"] = "Albert Einstein is a Physicist"
    #gives_and_gets["Are you evil"] = None

    tests_ok = True
    for give, get in gives_and_gets.items():
        if not give_and_get(give, get):
            tests_ok = False

    if tests_ok:
        print("All of " + str(len(gives_and_gets)) + " tests were OK.")
