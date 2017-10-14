# -*- coding: UTF-8 -*-

import unittest
from gi.repository import GObject, Gst
import thread
import logging
from decoder import DecoderPipeline
import time
import pyaudio # Provides Python bindings for PortAudio, the cross platform audio API

CHUNK = 8000 # Smallest unit of audio. 1024 bytes
FORMAT = pyaudio.paInt16 # Data format
CHANNELS = 1 # Number of channels
RATE = 16000 # Bit Rate of audio stream / Frame Rate
THRESHOLD = 1000 # Threshhold value for detecting stimulant
RECORD_SECONDS = 10

class KaldiRecognizer():

    def __init__(self):
        logging.basicConfig(level=logging.INFO)

        # voxforge/tri2b_mmi_b0.05 model:
        decoder_conf = {"model" : "models/english/final.mdl",
                        "lda-mat" : "models/english/final.mat",
                        "word-syms" : "models/english/words.txt",
                        "fst" : "models/english/HCLG.fst",
                        "silence-phones" : "6"}
        self.decoder_pipeline = DecoderPipeline({"decoder" : decoder_conf})
        self.__class__.words = []
        self.__class__.finished = False

        self.decoder_pipeline.set_word_handler(self.word_getter)
        self.decoder_pipeline.set_eos_handler(self.set_finished, self.finished)

        loop = GObject.MainLoop()
        thread.start_new_thread(loop.run, ())

    @classmethod
    def word_getter(self, word):
        self.words.append(word)

    @classmethod
    def set_finished(self, finished):
        self.finished = True

    def setUp(self):
        self.__class__.words = []
        self.__class__.finished = False



    def recognize(self):
        self.decoder_pipeline.init_request("recognize", "audio/x-raw, layout=(string)interleaved, rate=(int)16000, format=(string)S16LE, channels=(int)1")
        p = pyaudio.PyAudio() # Create a PyAudio session
        # Create a stream
        stream = p.open(format=FORMAT,
                    channels=CHANNELS,
                    rate=RATE,
                    input=True,
                    output=True,
                    frames_per_buffer=CHUNK)

        data = stream.read(CHUNK) # Get first data frame from the microphone
        for i in range(0, int(RATE / CHUNK * RECORD_SECONDS)):
            data = stream.read(CHUNK) # Read a new chunk from the stream
            stream.write(data, CHUNK)
            #time.sleep(0.25)
            self.decoder_pipeline.process_data(data)

        stream.stop_stream()
        stream.close()
        p.terminate()

        self.decoder_pipeline.end_request()
        while not self.finished:
            time.sleep(1)
        print self.words



if __name__ == '__main__':
    recognizer = KaldiRecognizer()
    recognizer.recognize()
