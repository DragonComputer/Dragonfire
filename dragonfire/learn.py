#!/usr/bin/python3
# -*- coding: utf-8 -*-

"""
.. module:: learn
    :platform: Unix
    :synopsis: the top-level submodule of Dragonfire that contains the classes related to Dragonfire's learning ability.

.. moduleauthor:: Mehmet Mert Yıldıran <mert.yildiran@bil.omu.edu.tr>
"""

import collections  # Imported to support ordered dictionaries in Python
from tinydb import TinyDB, Query  # TinyDB is a lightweight document oriented database
from os.path import expanduser  # Imported to get the home directory
from dragonfire.config import Config  # Credentials for the database connection
from dragonfire.database import Fact  # Submodule of Dragonfire module that contains the database schema
from sqlalchemy.orm.exc import NoResultFound  # the Python SQL toolkit and Object Relational Mapper


class Learner():
    """Class to provide the learning ability.
    """

    def __init__(self, nlp):
        """Initialization method of :class:`dragonfire.learn.Learner` class.

        Args:
            nlp:  :mod:`spacy` model instance.
        """

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
        self.db_session = None

    def respond(self, com, is_server=False, user_id=None):
        """Method to respond the user's input/command using learning ability.

        Args:
            com (str):  User's command.

        Keyword Args:
            is_server (bool):   Is Dragonfire running as an API server?
            user_id (int):      User's ID.

        Returns:
            str:  Response.

        .. note::

            Entry function for :class:`Learner` class. Dragonfire calls only this function. It does not handle TTS.

        """

        self.is_server = is_server
        is_public = True
        com = self.clean(com)
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
        subject = [x.strip() for x in subject]
        subject = ' '.join(subject)  # concatenate all noun phrases found
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

    def db_get(self, subject, invert=False, is_public=True, user_id=None):
        """Function to get a record from the database.

        Args:
            subject (str):  Subject that extracted from the user's input/command.

        Keyword Args:
            invert (bool):      Is it invert mode? (swap subject and clause)
            is_public (int):    Is it a public record? (non-user specific)
            user_id (int):      User's ID.

        Returns:
            str:  Response.
        """

        if self.is_server:
            try:
                if invert:
                    fact = self.db_session.query(Fact).filter(Fact.clause == subject, Fact.user_id == user_id, Fact.is_public == is_public).order_by(Fact.counter.desc()).first()
                else:
                    fact = self.db_session.query(Fact).filter(Fact.subject == subject, Fact.user_id == user_id, Fact.is_public == is_public).order_by(Fact.counter.desc()).first()
                answer = fact.subject + ' ' + fact.verbtense + ' ' + fact.clause
                return self.mirror(answer)
            except NoResultFound:
                return None
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

    def db_upsert(self, subject, verbtense, clause, com, is_public=True, user_id=None):
        """Function to insert(or update) a record to the database.

        Args:
            subject (str):      Subject that extracted from the user's input/command.
            verbtense (str):    The am/is/are in the user's input/command.
            clause (str):       Clause that contains the fact.
            com (str):          User's command.

        Keyword Args:
            invert (bool):      Is it invert mode? (swap subject and clause)
            is_public (int):    Is it a public record? (non-user specific)
            user_id (int):      User's ID.

        Returns:
            str:  Response.
        """

        if self.is_server:
            fact = self.db_session.query(Fact).filter(Fact.subject == subject, Fact.verbtense == verbtense, Fact.clause == clause, Fact.user_id == user_id, Fact.is_public == is_public).one_or_none()
            if not fact:
                new_fact = Fact(subject=subject, verbtense=verbtense, clause=clause, user_id=user_id, is_public=is_public)
                self.db_session.add(new_fact)
                self.db_session.commit()
            else:
                fact.counter += 1
                self.db_session.commit()
        else:
            if not self.db.search((Query().subject == subject) & (Query().verbtense == verbtense) & (Query().clause == clause)):  # if there is no exacty record on the database then
                self.db.insert({
                    'subject': subject,
                    'verbtense': verbtense,
                    'clause': clause
                })  # insert the given data
        return "OK, I get it. " + self.mirror(com)  # mirror the command(user's speech) and return it to say

    def db_delete(self, subject, is_public=True, user_id=None):
        """Function to delete a record from the database.

        Args:
            subject (str):  Subject that extracted from the user's input/command.

        Keyword Args:
            is_public (int):    Is it a public record? (non-user specific)
            user_id (int):      User's ID.

        Returns:
            str: Response.
        """

        if self.is_server:
            if not is_public and user_id:
                fact = self.db_session.query(Fact).filter(Fact.subject == subject, Fact.user_id == user_id).one_or_none()
                if not fact:
                    return "I don't even know anything about " + self.mirror(subject)
                else:
                    fact.delete()
                    self.db_session.commit()
                    return "OK, I forgot everything I know about " + self.mirror(subject)
            else:
                return "I cannot forget a general fact about " + self.mirror(subject)
        else:
            if self.db.remove(Query().subject == self.fix_pronoun(subject)):
                return "OK, I forgot everything I know about " + self.mirror(subject)
            else:
                return "I don't even know anything about " + self.mirror(subject)

    def mirror(self, answer):
        """Function to mirror the answer (for example: I'M to YOU ARE).

        Args:
            answer (str):  Prepared answer that just before the actual return of :func:`respond` method.

        Returns:
            str:  Response.
        """

        result = []
        types = []
        types.append("")
        doc = self.nlp(answer)
        for token in doc:
            types.append(token.lemma_)
            if token.lemma_ == "-PRON-":  # if it's a pronoun, mirror it
                if token.text.upper() in self.pronouns:
                    result.append(self.pronouns[token.text.upper()].lower().strip())
                    continue
                if token.text.upper() in self.inv_pronouns:
                    result.append(self.inv_pronouns[token.text.upper()].lower().strip())
                    continue
            if (token.lemma_ == "be" or token.dep_ == "aux") and types[-2] == "-PRON-":  # if it's an auxiliary that comes right after a pronoun, mirror it
                if token.text.upper() in self.auxiliaries:
                    result.append(self.auxiliaries[token.text.upper()].lower().strip())
                    continue
                if token.text.upper() in self.inv_auxiliaries:
                    result.append(self.inv_auxiliaries[token.text.upper()].lower().strip())
                    continue
            result.append(token.text.strip())
        for i in range(len(result)):
            if result[i] == "i":
                result[i] = "I"
        result = ' '.join(result)  # concatenate the result
        return result.replace(" '", "'")  # fix for situations like "I 'AM", "YOU 'LL"

    def fix_pronoun(self, subject):  # TODO: Extend the context of this function
        """Pronoun fixer to handle situations like YOU and YOURSELF.

        Args:
            subject (str):  Subject that extracted from the user's input/command.

        Returns:
            str:  Response.
        """

        if subject == "yourself":
            return "you"
        elif subject == "Yourself":
            return "You"
        elif subject == "YOURSELF":
            return "YOU"
        else:
            return subject

    def detect_pronoun(self, noun_chunk):
        """Determine whether user is talking about himself/herself or some other entity.

        Args:
            noun_chunk (str):  Noun phrase.

        Returns:
            ((str), (bool)):  Detected pronoun and boolean value depends on the detection.
        """

        np_text = ""
        is_public = True
        doc = self.nlp(noun_chunk)
        for token in doc:
            if token.lemma_ == "-PRON-":
                np_text += ' ' + token.text.lower()
                is_public = False
            else:
                np_text += ' ' + token.text
        return np_text.strip(), is_public

    def upper_capitalize(self, array):
        """Return capitalized and uppercased versions of the strings inside the given array.

        Args:
            array ((list) of (str)s):  List of strings.

        Returns:
            (list) of (str)s:  List of strings.
        """

        result = []
        for word in array:
            result.append(word)
            result.append(word.capitalize())
            result.append(word.upper())
        return result

    def clean(self, com):
        """Return a version of user's command that cleaned from punctuations, symbols, etc.

        Args:
            com (str):  User's command.

        Returns:
            str:  Cleaned version of user's command.
        """

        doc = self.nlp(com)
        for token in doc:
            if token.pos_ in ["PUNCT", "SYM"]:
                com = com.replace(token.tag_, '')

        return com
