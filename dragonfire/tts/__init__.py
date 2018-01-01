from __future__ import print_function
__author__ = 'Mehmet Mert Yildiran, mert.yildiran@bil.omu.edu.tr'
# This submodule is experimental and not functional

# CSV (Comma Separated Values) format is the most common import and export
# format for spreadsheets and databases
import csv
import glob
import pyaudio
import wave
import time

FORMAT = 8  # Data format
CHANNELS = 1  # Number of channels
RATE = 44100  # Bit Rate of audio stream / Frame Rate


class Synthesizer():
    def __init__(self):
        self.word_map = {}
        self.phonemes_map = {}

        filename = "../../dictionaries/VoxForgeDict"
        for line in csv.reader(
                open(filename), delimiter=' ', skipinitialspace=True):
            if len(line) > 2:
                self.word_map[line[0]] = line[2:]

        for file in glob.glob("phonemes/*.wav"):
            wf = wave.open(file, 'rb')
            n_frames = wf.getnframes()
            self.phonemes_map[file[9:][:-4]] = wf.readframes(n_frames)

    def string_to_phonemes(self, string):
        string = string.upper()
        string = string.replace('.', '')
        string = string.replace(',', '')
        words = string.split()

        result = []
        for word in words:
            if word in self.word_map:
                result.append(self.word_map[word])
        return result

    def run(self, string):
        skip = 4096
        audio = ""
        p = pyaudio.PyAudio()
        stream = p.open(
            format=FORMAT, channels=CHANNELS, rate=RATE, output=True)
        words = self.string_to_phonemes(string)
        print(words)
        for word in words:
            audio += ('\x00' * 20000)
            i = 0
            for phoneme in word:
                i += 1
                if i == 1 and i == len(self.phonemes_map[phoneme]):
                    audio += self.phonemes_map[phoneme]
                elif i == 1:
                    audio += self.phonemes_map[phoneme][:-skip]
                elif i == len(self.phonemes_map[phoneme]):
                    audio += self.phonemes_map[phoneme][skip:]
                else:
                    audio += self.phonemes_map[phoneme][skip:-skip]
                # audio += self.phonemes_map[phoneme]
        stream.write(audio)

        wf = wave.open(repr(time.time()).replace('.', '_') + ".wav",
                       'wb')  # Create the .wav file with a random name
        wf.setnchannels(CHANNELS)  # Set number of channels
        wf.setsampwidth(p.get_sample_size(FORMAT))  # Set sampling format
        wf.setframerate(RATE)  # Set Bit Rate / Frame Rate
        wf.writeframes(audio)  # Write the all frames of training_data
        wf.close()  # Close the session


if __name__ == "__main__":
    syn = Synthesizer()
    syn.run("I have a female voice but I don't have a gender identity.  "
            "I'm a computer program, sir.")
