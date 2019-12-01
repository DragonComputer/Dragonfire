#!/usr/bin/python3
# -*- coding: utf-8 -*-

"""
.. module:: omniscient
    :platform: Unix
    :synopsis: the top-level submodule of Dragonfire that contains the classes related to **Omniscient**: Dragonfire's Factoid Question Answering Engine.

.. moduleauthor:: Mehmet Mert Yıldıran <mert.yildiran@bil.omu.edu.tr>
"""

import collections  # Imported to support ordered dictionaries in Python
from random import uniform  # Generate pseudo-random numbers

from dragonfire.utilities import nostderr  # With statement to suppress errors

import requests.exceptions  # HTTP for Humans
import wikipedia  # Provides and API-like functionality to search and access Wikipedia data
import wikipedia.exceptions  # Exceptions of wikipedia library
from nltk.corpus import wordnet as wn  # The WordNet corpus
from nltk.corpus.reader.wordnet import WordNetError  # To catch the errors

from deeppavlov import build_model, configs


class Omniscient():
    """Class to provide the factoid question answering ability.
    """

    def __init__(self, nlp):
        """Initialization method of :class:`dragonfire.omniscient.Omniscient` class.

        Args:
            nlp:  :mod:`spacy` model instance.
        """

        self.nlp = nlp  # Load en_core_web_sm, English, 50 MB, default model
        self.model = build_model(configs.squad.squad, download=True)

    def respond(self, com, tts_output=False, userin=None, user_prefix=None, is_server=False):
        """Method to respond the user's input/command using factoid question answering ability.

        Args:
            com (str):  User's command.

        Keyword Args:
            tts_output (bool):      Is text-to-speech output enabled?
            userin:                 :class:`dragonfire.utilities.TextToAction` instance.
            user_prefix (str):      Prefix to address/call user when answering.
            is_server (bool):       Is Dragonfire running as an API server?

        Returns:
            str:  Response.

        .. note::

            Entry function for :class:`Omniscient` class. Dragonfire calls only this function. Unlike :func:`Learner.respond`, it executes TTS because of its late reponse nature.

        """

        result = None
        subject, subjects, focus, subject_with_objects = self.semantic_extractor(com)  # Extract the subject, focus, objects etc.
        if not subject:
            return False

        doc = self.nlp(com)  # spaCy does all kinds of NLP analysis in one function
        query = subject  # Wikipedia search query (same as the subject)
        # This is where the real search begins
        if query:  # If there is a Wikipedia query determined
            if not tts_output and not is_server: print("Please wait...")
            if tts_output and not is_server: userin.say("Please wait...", True, False)  # Gain a few more seconds by saying Please wait...
            wh_question = []
            for word in doc:  # Iterate over the words in the command(user's speech)
                if word.tag_ in ['WDT', 'WP', 'WP$', 'WRB']:  # if there is a wh word then
                    wh_question.append(word.text.upper())  # append it by converting to uppercase
            if not wh_question:
                return False
            with nostderr():
                try:
                    wikiresult = wikipedia.search(query)  # run a Wikipedia search with the query
                    if len(wikiresult) == 0:  # if there are no results
                        result = "Sorry, " + user_prefix + ". But I couldn't find anything about " + query + " in Wikipedia."
                        if not tts_output and not is_server: print(result)
                        if tts_output and not is_server: userin.say(result)
                        return result

                    wikipage = wikipedia.page(wikiresult[0])
                    return self.model([wikipage.content], [com])[0][0]
                except requests.exceptions.ConnectionError:  # if there is a connection error
                    result = "Sorry, " + user_prefix + ". But I'm unable to connect to Wikipedia servers."
                    if not is_server:
                        userin.execute([" "], "Wikipedia connection error.")
                        if not tts_output: print(result)
                        if tts_output: userin.say(result)
                    return result
                except wikipedia.exceptions.DisambiguationError as disambiguation:  # if there is a disambiguation
                    wikiresult = wikipedia.search(disambiguation.options[0])  # run Wikipedia search again with the most common option
                except:
                    result = "Sorry, " + user_prefix + ". But something went horribly wrong while I'm searching Wikipedia."
                    if not tts_output and not is_server: print(result)
                    if tts_output and not is_server: userin.say(result)
                    return result

    def phrase_cleaner(self, phrase):
        """Function to clean unnecessary words from the given phrase/string. (Punctuation mark, symbol, unknown, conjunction, determiner, subordinating or preposition and space)

        Args:
            phrase (str):  Noun phrase.

        Returns:
            str:  Cleaned noun phrase.
        """

        clean_phrase = []
        for word in self.nlp(phrase):
            if word.pos_ not in ['PUNCT', 'SYM', 'X', 'CONJ', 'DET', 'ADP', 'SPACE']:
                clean_phrase.append(word.text)
        return ' '.join(clean_phrase)

    def semantic_extractor(self, string):
        """Function to extract subject, subjects, focus, subject_with_objects from given string.

        Args:
            string (str):  String.

        Returns:
            (list) of (str)s: List of subject, subjects, focus, subject_with_objects.
        """

        doc = self.nlp(string)  # spaCy does all kinds of NLP analysis in one function
        the_subject = None  # Wikipedia search query variable definition (the subject)
        # Followings are lists because it could be multiple of them in a string. Multiple objects or subjects...
        subjects = []  # subject list
        pobjects = []  # object of a preposition list
        dobjects = []  # direct object list
        # https://nlp.stanford.edu/software/dependencies_manual.pdf - Hierarchy of typed dependencies
        for np in doc.noun_chunks:  # Iterate over the noun phrases(chunks)
            # print(np.text, np.root.text, np.root.dep_, np.root.head.text)
            if (np.root.dep_ == 'nsubj' or np.root.dep_ == 'nsubjpass') and np.root.tag_ != 'WP':  # if it's a nsubj(nominal subject) or nsubjpass(passive nominal subject) then
                subjects.append(np.text)  # append it to subjects
            if np.root.dep_ == 'pobj':  # if it's an object of a preposition then
                pobjects.append(np.text)  # append it to pobjects
            if np.root.dep_ == 'dobj':  # if it's a direct object then
                dobjects.append(np.text)  # append it to direct objects

        # This block determines the Wikipedia query (the subject) by relying on this priority: [Object of a preposition] > [Subject] > [Direct object]
        pobjects = [x for x in pobjects]
        subjects = [x for x in subjects]
        dobjects = [x for x in dobjects]
        if pobjects:
            the_subject = ' '.join(pobjects)
        elif subjects:
            the_subject = ' '.join(subjects)
        elif dobjects:
            the_subject = ' '.join(dobjects)
        else:
            return None, None, None, None

        # This block determines the focus(objective/goal) by relying on this priority: [Direct object] > [Subject] > [Object of a preposition]
        focus = None
        if dobjects:
            focus = self.phrase_cleaner(' '.join(dobjects))
        elif subjects:
            focus = self.phrase_cleaner(' '.join(subjects))
        elif pobjects:
            focus = self.phrase_cleaner(' '.join(pobjects))
        if focus in the_subject:
            focus = None

        # Full string of all subjects and objects concatenated
        subject_with_objects = []
        for dobject in dobjects:
            subject_with_objects.append(dobject)
        for subject in subjects:
            subject_with_objects.append(subject)
        for pobject in pobjects:
            subject_with_objects.append(pobject)
        subject_with_objects = ' '.join(subject_with_objects)

        wh_found = False
        for word in doc:  # iterate over the each word in the given command(user's speech)
            if word.tag_ in ['WDT', 'WP', 'WP$', 'WRB']:  # check if there is a "wh-" question (we are determining that if it's a question or not, so only accepting questions with "wh-" form)
                wh_found = True
        if not wh_found:
            return None, None, None, None

        return the_subject, subjects, focus, subject_with_objects
