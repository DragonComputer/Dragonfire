#!/usr/bin/python3
# -*- coding: utf-8 -*-

"""
.. module:: nlplib
    :platform: Unix
    :synopsis: the top-level submodule of Dragonfire that contains the classes to provide an extra layer of abstraction to the NLP libraries that are used by Dragonfire.

.. moduleauthor:: Mehmet Mert Yıldıran <mert.yildiran@bil.omu.edu.tr>
"""

from random import shuffle  # Generate pseudo-random numbers

import nltk  # Natural Language Toolkit
from nltk.corpus import names  # The Names Corpus
from nltk.corpus import brown  # The Brown Corpus


class Classifier():
    """Class to provide static classification methods for various NLP tasks.
    """

    @staticmethod
    def gender_features(word):
        if not word:
            return {'last_letter': 'a'}
        else:
            return {'last_letter': word[-1]}

    @staticmethod
    def gender(word):
        """Method to determine the gender of given word by comparing it to name dictionaries.

        Args:
            word (str):  Word. (usually a name)

        Keyword Args:
            is_server (bool):   Is Dragonfire running as an API server?
            user_id (int):      User's ID.

        Returns:
            str:  Male or Female

        .. note::

            This method is a very naive and not very useful. So it will be deprecated in the future.

        """

        labeled_names = ([(name, 'male') for name in names.words('male.txt')] +
                         [(name, 'female')
                          for name in names.words('female.txt')])
        shuffle(labeled_names)
        featuresets = [(Classifier.gender_features(n), gender)
                       for (n, gender) in labeled_names]
        train_set = featuresets[500:]
        classifier = nltk.NaiveBayesClassifier.train(train_set)
        return classifier.classify(Classifier.gender_features(word))


class TopicExtractor(object):
    """Class to provide methods to extrac the topic from given sentence using NLTK library.
    """

    def __init__(self):
        """Initialization method of :class:`TopicExtractor` class.
        """

        # This is our fast Part of Speech tagger
        #############################################################################
        brown_train = brown.tagged_sents(categories='news')
        regexp_tagger = nltk.RegexpTagger(
            [(r'^-?[0-9]+(.[0-9]+)?$', 'CD'),
                (r'(-|:|;)$', ':'),
                (r'\'*$', 'MD'),
                (r'(The|the|A|a|An|an)$', 'AT'),
                (r'.*able$', 'JJ'),
                (r'^[A-Z].*$', 'NNP'),
                (r'.*ness$', 'NN'),
                (r'.*ly$', 'RB'),
                (r'.*s$', 'NNS'),
                (r'.*ing$', 'VBG'),
                (r'.*ed$', 'VBD'),
                (r'.*', 'NN')
            ])
        unigram_tagger = nltk.UnigramTagger(brown_train, backoff=regexp_tagger)
        self.bigram_tagger = nltk.BigramTagger(brown_train, backoff=unigram_tagger)
        #############################################################################

        # This is our semi-CFG; Extend it according to your own needs
        #############################################################################
        self.cfg = {}
        self.cfg["NNP+NNP"] = "NNP"
        self.cfg["NN+NN"] = "NNI"
        self.cfg["NNI+NN"] = "NNI"
        self.cfg["JJ+JJ"] = "JJ"
        self.cfg["JJ+NN"] = "NNI"

        #############################################################################

    def tokenize_sentence(self, sentence):
        """Tokenize the given sentence.

        Split the sentence into single words/tokens.

        Args:
            sentence (str):  A sentence.

        Returns:
            (list) of (str)s:  List of strings.
        """

        tokens = nltk.word_tokenize(sentence)
        return tokens

    def normalize_tags(self, tagged):
        """Normalize brown corpus' tags `("NN", "NN-PL", "NNS" -> "NN")`.

        Args:
            tagged ((list) of (str)s):  Tagged words.

        Returns:
            (list) of (str)s:  List of strings.
        """

        n_tagged = []
        for t in tagged:
            if t[1] in ("NP-TL", "NP"):
                n_tagged.append((t[0], "NNP"))
                continue
            if t[1].endswith("-TL"):
                n_tagged.append((t[0], t[1][:-3]))
                continue
            if t[1].endswith("S"):
                n_tagged.append((t[0], t[1][:-1]))
                continue
            n_tagged.append((t[0], t[1]))
        return n_tagged

    def extract(self, sentence):
        """Extract the main topics from the sentence.

        Returns:
            (list) of (str)s:  List of strings.
        """

        tokens = self.tokenize_sentence(sentence)
        tags = self.normalize_tags(self.bigram_tagger.tag(tokens))

        merge = True
        while merge:
            merge = False
            for x in range(0, len(tags) - 1):
                t1 = tags[x]
                t2 = tags[x + 1]
                key = "%s+%s" % (t1[1], t2[1])
                value = self.cfg.get(key, '')
                if value:
                    merge = True
                    tags.pop(x)
                    tags.pop(x)
                    match = "%s %s" % (t1[0], t2[0])
                    pos = value
                    tags.insert(x, (match, pos))
                    break

        matches = []
        for t in tags:
            if t[1] == "NNP" or t[1] == "NNI":
                # if t[1] == "NNP" or t[1] == "NNI" or t[1] == "NN":
                matches.append(t[0])
        return matches


class Helper():
    """Class to provide an extra layer of abstraction to the :mod:`spacy` NLP library.
    """

    def __init__(self, doc):
        """Initialization method of :class:`dragonfire.nlplib.Helper` class.

        Args:
            doc:  :class:`Doc` instance from spaCy NLP library. Pre-parsed version of user's input/command.
        """

        self.doc = doc

    def directly_equal(self, words):
        """Method to check if user's input is directly equal to one of these words.

        Args:
            words ((list) of (str)s):  Words.

        Returns:
            bool:  True or False
        """

        for word in words:
            if self.doc[0].lemma_ == word.lower() and len(self.doc) == 1:
                return True
        return False

    def check_nth_lemma(self, n, word):
        """Method to check if nth lemma is equal to given word.

        Args:
            n (int):        nth lemma.
            word (str):     Word.

        Returns:
            bool:  True or False
        """

        try:
            return self.doc[n].lemma_ == word
        except IndexError:
            return False

    def check_verb_lemma(self, verb):
        """Method to check if there is a verb with given lemma.

        Args:
            verb (str):  Verb lemma.

        Returns:
            bool:  True or False
        """

        for token in self.doc:
            if token.pos_ == "VERB" and token.lemma_ == verb:
                return True
        return False

    def check_wh_lemma(self, wh):
        """Method to check if there is a WH- word with given lemma.

        Args:
            wh (str):  WH- word lemma.

        Returns:
            bool:  True or False
        """

        for token in self.doc:
            if token.tag_ in ['WDT', 'WP', 'WP$', 'WRB'] and token.lemma_ == wh:
                return True
        return False

    def check_deps_contains(self, phrase):
        """Method to check if the user's input/command contains this phrase.

        Args:
            phrase (str):  Noun phrase.

        Returns:
            bool:  True or False
        """

        for chunk in self.doc.noun_chunks:
            if chunk.text.lower() == phrase.lower():
                return True
        return False

    def check_only_dep_is(self, phrase):
        """Method to check if this is the only phrase user's input/command has.

        Args:
            phrase (str):  Noun phrase.

        Returns:
            bool:  True or False
        """

        return sum(1 for _ in self.doc.noun_chunks) == 1 and self.doc.noun_chunks.__next__().text.lower() == phrase.lower()

    def check_noun_lemma(self, noun):
        """Method to check if there is a verb noun given lemma.

        Args:
            noun (str):  Noun lemma.

        Returns:
            bool:  True or False
        """

        for token in self.doc:
            if (token.pos_ == "NOUN" or token.pos_ == "PROPN") and token.lemma_ == noun:
                return True
        return False

    def check_adj_lemma(self, adj):
        """Method to check if there is an adjective with given lemma.

        Args:
            adj (str):  Adjective lemma.

        Returns:
            bool:  True or False
        """

        for token in self.doc:
            if token.pos_ == "ADJ" and token.lemma_ == adj:
                return True
        return False

    def check_adv_lemma(self, adv):
        """Method to check if there is an adverb with given lemma.

        Args:
            adv (str):  Adverb lemma.

        Returns:
            bool:  True or False
        """

        for token in self.doc:
            if token.pos_ == "ADV" and token.lemma_ == adv:
                return True
        return False

    def check_lemma(self, lemma):
        """Method to check if there is a word with given lemma.

        Args:
            lemma (str):  Lemma.

        Returns:
            bool:  True or False
        """

        for token in self.doc:
            if token.lemma_ == lemma:
                return True
        return False

    def check_text(self, text):
        """Method to check if the user's input/command is directly equal to given text.

        Args:
            text (str):  Text.

        Returns:
            bool:  True or False
        """

        for token in self.doc:
            if token.text.upper() == text.upper():
                return True
        return False

    def is_wh_question(self):
        """Method to check if the user's input/command a WH question.

        Returns:
            bool:  True or False
        """

        for token in self.doc:
            if token.is_stop:
                break
            if token.tag_ in ['WDT', 'WP', 'WP$', 'WRB']:
                return True
        return False

    def max_word_count(self, n):
        """Method to check if the word length of the user's input/command is less than or equal to given value.

        Args:
            n (int):  Number of words.

        Returns:
            bool:  True or False
        """

        return len(self.doc) <= n
