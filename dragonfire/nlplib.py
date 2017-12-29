#!/usr/bin/python
# -*- coding: utf-8 -*-

from __future__ import print_function
import nltk
from nltk.corpus import names
from nltk.corpus import brown
import random


class Classifiers():
    @staticmethod
    def gender_features(word):
        return {'last_letter': word[-1]}

    @staticmethod
    def gender(word):
        labeled_names = ([(name, 'male') for name in names.words('male.txt')] +
                         [(name, 'female')
                          for name in names.words('female.txt')])
        random.shuffle(labeled_names)
        featuresets = [(Classifiers.gender_features(n), gender)
                       for (n, gender) in labeled_names]
        train_set = featuresets[500:]
        classifier = nltk.NaiveBayesClassifier.train(train_set)
        return classifier.classify(Classifiers.gender_features(word))


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


if __name__ == "__main__":
    print(Classifiers.gender("Mehmet"))
    print(Classifiers.gender("Ayşe"))
    print(Classifiers.gender("İsmail"))
    print(Classifiers.gender("Berna"))

    sentence = "Do you know the birthdate of Barrack Obama"
    topic_obj = TopicExtractor(sentence)
    result = topic_obj.extract()
    print("This sentence is about: %s" % ", ".join(result))
