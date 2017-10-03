__author__ = 'Mehmet Mert Yildiran, mert.yildiran@bil.omu.edu.tr'

import csv # CSV (Comma Separated Values) format is the most common import and export format for spreadsheets and databases

CHUNK = 1024 # Smallest unit of audio. 1024 bytes
FORMAT = pyaudio.paInt16 # Data format
CHANNELS = 2 # Number of channels
RATE = 44100 # Bit Rate of audio stream / Frame Rate

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

        result = []
        for word in words:
            if word in self.word_map:
                result.append(self.word_map[word])
        return result


if __name__ == "__main__":
    syn = Synthesizer()
    print syn.string_to_phonemes("I have a female voice but I don't have a gender identity. I'm a computer program, sir.")
