import csv


class Synthesizer():

    def __init__(self):
        self.word_map = {}

        filename = "../../dictionaries/VoxForgeDict"
        for line in csv.reader(open(filename), delimiter=' ', skipinitialspace=True):
            if len(line) > 2:
                self.word_map[line[0]] = line[2:]
        print len(self.word_map)

    def string_to_phonemes(self, string):
        string = string.upper()
        string = string.replace('.','')
        string = string.replace(',','')
        words = string.split()

        result = ""
        for word in words:
            print self.word_map[word]
