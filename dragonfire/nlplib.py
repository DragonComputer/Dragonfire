#!/usr/bin/python
# -*- coding: utf-8 -*-

from __future__ import print_function
import nltk
from nltk.corpus import names
from nltk.corpus import brown
import random


class Classifier():
    @staticmethod
    def gender_features(word):
        if not word:
            return {'last_letter': 'a'}
        else:
            return {'last_letter': word[-1]}

    @staticmethod
    def gender(word):
        labeled_names = ([(name, 'male') for name in names.words('male.txt')] +
                         [(name, 'female')
                          for name in names.words('female.txt')])
        random.shuffle(labeled_names)
        featuresets = [(Classifier.gender_features(n), gender)
                       for (n, gender) in labeled_names]
        train_set = featuresets[500:]
        classifier = nltk.NaiveBayesClassifier.train(train_set)
        return classifier.classify(Classifier.gender_features(word))


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
bigram_tagger = nltk.BigramTagger(brown_train, backoff=unigram_tagger)
#############################################################################

# This is our semi-CFG; Extend it according to your own needs
#############################################################################
cfg = {}
cfg["NNP+NNP"] = "NNP"
cfg["NN+NN"] = "NNI"
cfg["NNI+NN"] = "NNI"
cfg["JJ+JJ"] = "JJ"
cfg["JJ+NN"] = "NNI"

#############################################################################


class TopicExtractor(object):
    def __init__(self, sentence):
        self.sentence = sentence

    # Split the sentence into singlw words/tokens
    def tokenize_sentence(self, sentence):
        tokens = nltk.word_tokenize(sentence)
        return tokens

    # Normalize brown corpus' tags ("NN", "NN-PL", "NNS" > "NN")
    def normalize_tags(self, tagged):
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

    # Extract the main topics from the sentence
    def extract(self):

        tokens = self.tokenize_sentence(self.sentence)
        tags = self.normalize_tags(bigram_tagger.tag(tokens))

        merge = True
        while merge:
            merge = False
            for x in range(0, len(tags) - 1):
                t1 = tags[x]
                t2 = tags[x + 1]
                key = "%s+%s" % (t1[1], t2[1])
                value = cfg.get(key, '')
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

    def __init__(self, doc):
        self.doc = doc

    def directly_equal(self, words):
        for word in words:
            if self.doc[0].lemma_ == word and len(self.doc) == 1:
                return True
        return False

    def check_nth_lemma(self, n, word):
        return self.doc[n].lemma_ == word

    def check_verb_lemma(self, verb):
        for token in self.doc:
            if token.pos_ == "VERB" and token.lemma_ == verb:
                return True
        return False

    def check_wh_lemma(self, wh):
        for token in self.doc:
            if token.tag_ in ['WDT', 'WP', 'WP$', 'WRB'] and token.lemma_ == wh:
                return True
        return False

    def check_deps_contains(self, phrase):
        for chunk in self.doc.noun_chunks:
            if chunk.text == phrase:
                return True
        return False

    def check_only_dep_is(self, phrase):
        return len(self.doc.noun_chunks) == 1 and self.doc.noun_chunks[0].text == phrase

    def check_noun_lemma(self, noun):
        for token in self.doc:
            if (token.pos_ == "NOUN" or token.pos_ == "PROPN") and token.lemma_ == noun:
                return True
        return False

    def check_adj_lemma(self, adj):
        for token in self.doc:
            if token.pos_ == "ADJ" and token.lemma_ == adj:
                return True
        return False

    def check_lemma(self, lemma):
        for token in self.doc:
            if token.lemma_ == lemma:
                return True
        return False

    def check_text(self, text):
        for token in self.doc:
            if token.text.upper() == text.upper():
                return True
        return False

    def is_wh_question(self):
        for token in self.doc:
            if token.tag_ in ['WDT', 'WP', 'WP$', 'WRB']:
                return True
        return False

    def max_word_count(self, n):
        return len(self.doc) <= n


if __name__ == "__main__":
    print(Classifier.gender("James"))
    print(Classifier.gender("Robert"))
    print(Classifier.gender("Mary"))
    print(Classifier.gender("Linda"))

    sentence = "Do you know the birthdate of Barrack Obama"
    topic_obj = TopicExtractor(sentence)
    result = topic_obj.extract()
    print("This sentence is about: %s" % ", ".join(result))
