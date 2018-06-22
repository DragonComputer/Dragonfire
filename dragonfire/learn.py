from __future__ import print_function
import collections  # Imported to support ordered dictionaries in Python
from tinydb import TinyDB, Query  # TinyDB is a lightweight document oriented database
from os.path import expanduser  # Imported to get the home directory
from dragonfire.config import Config
import pymysql


class Learner():
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
        self.db = TinyDB(home + '/.dragonfire_db.json')  # This is where we store the database; /home/USERNAME/.dragonfire_db.json
        self.nlp = nlp  # Load en_core_web_sm, English, 50 MB, default model
        self.is_server = False

    # Entry function for this class. Dragonfire calls only this function. It does not handle TTS.
    def respond(self, com, is_server=False, user_id=None):
        self.is_server = is_server
        is_public = True
        doc = self.nlp(com)  # Command(user's speech) must be decoded from utf-8 to unicode because spaCy only supports unicode strings, self.nlp() handles all parsing
        subject = []  # subject list (subjects here usually are; I'M, YOU, HE, SHE, IT, etc.)
        types = []  # types of the previous noun phrases
        types.append("")
        for np in doc.noun_chunks:  # Iterate over the noun phrases(chunks) TODO: Cover 'dobj' also; doc = nlp(u'DESCRIBE THE SUN') >>> (u'THE SUN', u'SUN', u'dobj', u'DESCRIBE')
            types.append(np.root.dep_)
            np_text, is_public = self.detect_pronoun(np.text)
            # print("IS_PUBLIC: ", is_public)
            # Purpose of this if statement is completing possessive form of nouns
            if np.root.dep_ == 'pobj' and types[-2] == 'nsubj':  # if it's an object of a preposition and the previous noun phrase's type was nsubj(nominal subject) then (it's purpose is capturing subject like MY PLACE OF BIRTH)
                subject.append(np.root.head.text)  # append the parent text from syntactic relations tree (example: while nsubj is 'MY PLACE', np.root.head.text is 'OF')
                subject.append(np_text)  # append the text of this noun phrase (example: while nsubj is 'MY PLACE', np.text is 'BIRTH')
            if np.root.dep_ == 'nsubj' and types[-2] not in ['pobj', 'nsubj'] and np.root.tag_ not in ['WDT', 'WP', 'WP$', 'WRB']:  # if it's a nsubj(nominal subject) ("wh-" words can be considered as nsubj(nominal subject) but they are out of scope.  This is why we are excluding them.)
                subject.append(np_text)  # append the text of this noun phrase
            if np.root.dep_ == 'attr' and types[-2] not in ['pobj', 'nsubj'] and np.root.tag_ not in ['WDT', 'WP', 'WP$', 'WRB']:  # if it's an attribute and the previous noun phrase's type was not nsubj(nominal subject)
                subject.append(np_text)  # append the text of this noun phrase
            if np.root.dep_ == 'dobj' and types[-2] not in ['pobj', 'nsubj'] and np.root.tag_ not in ['WDT', 'WP', 'WP$', 'WRB']:  # if it's a dobj(direct object) and the previous noun phrase's type was not nsubj(nominal subject)
                subject.append(np_text)  # append the text of this noun phrase
        subject = [x for x in subject]
        subject = ' '.join(subject).strip()  # concatenate all noun phrases found
        if subject:  # if the subject is not empty
            if subject.upper() in self.inv_pronouns:  # pass the learning ability if the user is talking about Dragonfire's itself
                return ""
            wh_found = False
            for word in doc:  # iterate over the each word in the given command(user's speech)
                if word.tag_ in ['WDT', 'WP', 'WP$', 'WRB']:  # check if there is a "wh-" question (we are determining that if it's a question or not, so only accepting questions with "wh-" form)
                    wh_found = True
            if wh_found:  # if that's a question
                straight = self.db_get(subject, is_public=is_public, user_id=user_id)  # get the answer from the database
                if straight is None:
                    return self.db_get(subject, is_public=is_public, user_id=user_id, invert=True)  # if nothing found then invert
                return straight
            else:
                verb_found = False
                verbtense = None  # verbtense is the am/is/are of the main sentence
                clause = []  # is the information that we need to acknowledge
                verbs = []
                for word in doc:
                    # print(word.text, word.lemma_, word.pos_, word.tag_, word.dep_, word.shape_, word.is_alpha, word.is_stop)
                    if verb_found:  # get the all words comes after the first verb which will be our verbtense
                        if word.pos_ != 'PUNCT':  # exclude punctuations
                            clause.append(word.text)
                    if word.pos_ == 'VERB' and word.is_stop and not verb_found:  # if that's a verb and verb does not found yet then
                        verb_found = True  # verb is found
                        verbtense = word.text  # append it to verbtense
                    if word.pos_ == 'VERB':
                        verbs.append(word.text)
                clause = [x for x in clause]
                clause = ' '.join(clause).strip()  # concatenate the clause

                # keywords to order get and remove operations on the database
                if any(verb in verbs for verb in self.upper_capitalize(["forget", "remove", "delete", "update"])):
                    if self.is_server and is_public:
                        return "I cannot forget a general fact."
                    return self.db_delete(subject, is_public=is_public, user_id=user_id)  # if there is a record about the subject in the database then remove that record and...

                if any(verb in verbs for verb in self.upper_capitalize(["define", "explain", "tell", "describe"])):
                    return self.db_get(subject, is_public=is_public, user_id=user_id)

                if verbtense:
                    return self.db_upsert(subject, verbtense, clause, com, is_public=is_public, user_id=user_id)  # set the record to the database

    # Function to get a record from the database
    def db_get(self, subject, invert=False, is_public=True, user_id=None):
        if self.is_server:
            u_id = 0
            if not is_public and user_id:
                u_id = user_id
            db = pymysql.connect(Config.MYSQL_HOST, Config.MYSQL_USER, Config.MYSQL_PASS, Config.MYSQL_DB)
            cursor = db.cursor(pymysql.cursors.DictCursor)
            if invert:
                sql = "SELECT * FROM facts WHERE clause = '{}' AND user_id = '{}' ORDER BY counter DESC".format(subject, u_id)
            else:
                sql = "SELECT * FROM facts WHERE subject = '{}' AND user_id = '{}' ORDER BY counter DESC".format(subject, u_id)
            try:
                cursor.execute(sql)
                results = cursor.fetchall()
                if not results:
                    return None
                row = results[0]
                answer = row['subject'] + ' ' + row['verbtense'] + ' ' + row['clause']
                return self.mirror(answer)
            except pymysql.InternalError as error:
                code, message = error.args
                print (">>>>>>>>>>>>>", code, message)
                return "Sorry, I encountered with a database problem."
            db.close()
        else:
            if invert:
                result = self.db.search(Query().clause == subject)  # make a database search by giving subject string (inverted)
            else:
                result = self.db.search(Query().subject == subject)  # make a database search by giving subject string
            if result:  # if there is a result
                dictionary = {}
                for row in result:  # iterate over the rows of the result
                    if row['verbtense'] not in dictionary:  # if the verbtense is not in the keys of the dictionary
                        dictionary[row['verbtense']] = []  # then add it
                    if row['clause'] not in dictionary[row['verbtense']]:  # if the clause is not in the value like; dictionary['is']
                        dictionary[row['verbtense']].append(row['clause'])  # then append the clause
                if invert:
                    answer = row['subject']  # in WHO questions subject is actually the clause so we learn the subject from db
                else:
                    answer = subject  # the answer we will return
                first_verbtense = False
                for key, value in dictionary.items():  # iterate over the dictionary defined and assigned on above
                    if not first_verbtense:  # if the first verbtense assignment does not made yet
                        answer += ' ' + str(key)  # concatenate with a whitespace
                        first_verbtense = True
                    else:
                        answer += ', ' + str(key)  # otherwise concatenate with a comma + whitespace
                    first_clause = False
                    for clause in value:  # iterate over the clauses of the key
                        if not first_clause:  # if the first verbtense assignment does not made yet
                            answer += ' ' + clause  # concatenate with a whitespace
                            first_clause = True
                        else:
                            answer += ' and ' + clause  # otherwise concatenate with ' AND '
                return self.mirror(answer)  # mirror the answer (for example: I'M to YOU ARE)
            else:
                return None  # if there is no result return None

    # Function to set a record to the database
    def db_upsert(self, subject, verbtense, clause, com, is_public=True, user_id=None):
        if self.is_server:
            u_id = 0
            if not is_public and user_id:
                u_id = user_id
            db = pymysql.connect(Config.MYSQL_HOST, Config.MYSQL_USER, Config.MYSQL_PASS, Config.MYSQL_DB)
            cursor = db.cursor(pymysql.cursors.DictCursor)
            sql1 = "SELECT * FROM facts WHERE subject = '{}' AND verbtense = '{}' AND clause = '{}' AND user_id = '{}'".format(subject, verbtense, clause, u_id)
            sql2 = """
                INSERT INTO facts (subject, verbtense, clause, user_id)
                VALUES('{}', '{}', '{}', '{}')
                """.format(subject, verbtense, clause, u_id)
            sql3 = """
                UPDATE facts
                SET counter = counter + 1
                WHERE subject = '{}' AND verbtense = '{}' AND clause = '{}' AND user_id = '{}'
            """.format(subject, verbtense, clause, u_id)
            try:
                cursor.execute(sql1)
                results = cursor.fetchall()
                if not results:
                    cursor.execute(sql2)
                    db.commit()
                else:
                    cursor.execute(sql3)
                    db.commit()
            except pymysql.InternalError as error:
                code, message = error.args
                print (">>>>>>>>>>>>>", code, message)
                return "Sorry, I encountered with a database problem."
            db.close()
        else:
            if not self.db.search((Query().subject == subject) & (Query().verbtense == verbtense) & (Query().clause == clause)):  # if there is no exacty record on the database then
                self.db.insert({
                    'subject': subject,
                    'verbtense': verbtense,
                    'clause': clause
                })  # insert the given data
        return "OK, I get it. " + self.mirror(com)  # mirror the command(user's speech) and return it to say

    # Function to delete a record from the database
    def db_delete(self, subject, is_public=True, user_id=None):
        if self.is_server:
            if not is_public and user_id:
                db = pymysql.connect(Config.MYSQL_HOST, Config.MYSQL_USER, Config.MYSQL_PASS, Config.MYSQL_DB)
                cursor = db.cursor(pymysql.cursors.DictCursor)
                sql1 = "SELECT * FROM facts WHERE subject = '{}' AND user_id = '{}'".format(subject, user_id)
                sql2 = "DELETE FROM facts WHERE subject = '{}' AND user_id = '{}'".format(subject, user_id)
                try:
                    cursor.execute(sql1)
                    results = cursor.fetchall()
                    if not results:
                        db.close()
                        return "I don't even know anything about " + self.mirror(subject)
                    else:
                        cursor.execute(sql2)
                        db.commit()
                        db.close()
                        return "OK, I forgot everything I know about " + self.mirror(subject)
                except pymysql.InternalError as error:
                    code, message = error.args
                    print (">>>>>>>>>>>>>", code, message)
                    return "Sorry, I encountered with a database problem."
            else:
                return "I don't even know anything about " + self.mirror(subject)
        else:
            if self.db.remove(Query().subject == self.fix_pronoun(subject)):
                return "OK, I forgot everything I know about " + self.mirror(subject)
            else:
                return "I don't even know anything about " + self.mirror(subject)

    # Function to mirror the answer (for example: I'M to YOU ARE)
    def mirror(self, answer):
        result = []
        types = []
        types.append("")
        doc = self.nlp(answer)
        for token in doc:
            types.append(token.lemma_)
            if token.lemma_ == "-PRON-":  # if it's a pronoun, mirror it
                if token.text.upper() in self.pronouns:
                    result.append(self.pronouns[token.text.upper()].lower())
                    continue
                if token.text.upper() in self.inv_pronouns:
                    result.append(self.inv_pronouns[token.text.upper()].lower())
                    continue
            if (token.lemma_ == "be" or token.dep_ == "aux") and types[-2] == "-PRON-":  # if it's an auxiliary that comes right after a pronoun, mirror it
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
        result = ' '.join(result)  # concatenate the result
        result = result.replace(" '", "'")  # fix for situations like "I 'AM", "YOU 'LL"
        return result

    # Pronoun fixer to handle situations like YOU and YOURSELF
    def fix_pronoun(self, subject):  # TODO: Extend the context of this function
        if subject == "yourself":
            return "you"
        elif subject == "Yourself":
            return "You"
        elif subject == "YOURSELF":
            return "YOU"
        else:
            return subject

    def detect_pronoun(self, noun_chunk):
        np_text = ""
        is_public = True
        doc = self.nlp(noun_chunk)
        for token in doc:
            if token.lemma_ == "-PRON-":
                np_text += ' ' + token.text.lower()
                is_public = False
            else:
                np_text += ' ' + token.text
        return np_text, is_public

    def upper_capitalize(self, array):
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
    home = expanduser("~")  # Get the home directory of the user
    if os.path.exists(home + '/.dragonfire_db.json'):
        os.remove(home + '/.dragonfire_db.json')  # This is where we store the database; /home/USERNAME/.dragonfire_db.json
    learner = Learner(spacy.load('en'))

    def give_and_get(give, get):
        result = learner.respond(give)
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
    # gives_and_gets["Are you evil"] = None

    tests_ok = True
    for give, get in gives_and_gets.items():
        if not give_and_get(give, get):
            tests_ok = False

    if tests_ok:
        print("All of " + str(len(gives_and_gets)) + " tests were OK.")
