# -*- coding: UTF-8 -*-

from __future__ import absolute_import

# Operates on sound fragments consisting of signed integer samples 8, 16
# or 32 bits wide, stored in Python strings.
import audioop
import os
import time
from contextlib import contextmanager
from ctypes import CFUNCTYPE, c_char_p, c_int, cdll
from threading import Thread

import pyaudio  # Provides Python bindings for PortAudio, the cross platform audio API
from dragonfire import VirtualAssistant
from gi.repository import GObject

from .decoder import DecoderPipeline

CHUNK = 8000  # Smallest unit of audio. 1024 bytes
FORMAT = pyaudio.paInt16  # Data format
CHANNELS = 1  # Number of channels
RATE = 16000  # Bit Rate of audio stream / Frame Rate
THRESHOLD = 1000  # Threshhold value for detecting stimulant
SILENCE_DETECTION = 5  # Wait number of frames to decide whether it fell silent or not
LISTENING = False
ENGLISH_MODEL_PATH = os.path.dirname(
    os.path.realpath(__file__)) + "/models/english/"


class KaldiRecognizer():
    def __init__(self):
        # logging.basicConfig(level=logging.INFO)

        # voxforge/tri2b_mmi_b0.05 model:
        decoder_conf = {
            "model": ENGLISH_MODEL_PATH + "final.mdl",
            "lda-mat": ENGLISH_MODEL_PATH + "final.mat",
            "word-syms": ENGLISH_MODEL_PATH + "words.txt",
            "fst": ENGLISH_MODEL_PATH + "HCLG.fst",
            "silence-phones": "6"
        }
        self.decoder_pipeline = DecoderPipeline({"decoder": decoder_conf})
        self.__class__.words = []
        self.__class__.finished = False

        self.decoder_pipeline.set_word_handler(self.word_getter)
        self.decoder_pipeline.set_eos_handler(self.set_finished, self.finished)

        GObject.threads_init()
        self.loop = GObject.MainLoop()
        self.gi_thread = Thread(target=self.loop.run, args=())
        self.gi_thread.start()

    @classmethod
    def word_getter(self, word):
        self.words.append(word)

    @classmethod
    def set_finished(self, finished):
        self.finished = True

    def reset(self):
        self.__class__.words = []
        self.__class__.finished = False

    def recognize(self, args):

        with noalsaerr():
            p = pyaudio.PyAudio()  # Create a PyAudio session
        # Create a stream
        stream = p.open(
            format=FORMAT,
            channels=CHANNELS,
            rate=RATE,
            input=True,
            output=True,
            frames_per_buffer=CHUNK)

        try:
            data = stream.read(
                CHUNK)  # Get first data frame from the microphone
            # Loop over the frames of the audio / data chunks
            while data != '':
                rms = audioop.rms(
                    data, 2)  # Calculate Root Mean Square of current chunk
                if rms >= THRESHOLD:  # If Root Mean Square value is greater than THRESHOLD constant
                    self.decoder_pipeline.init_request(
                        "recognize",
                        "audio/x-raw, layout=(string)interleaved, rate=(int)16000, format=(string)S16LE, channels=(int)1"
                    )
                    self.decoder_pipeline.process_data(data)
                    silence_counter = 0  # Define silence counter
                    # While silence counter value less than SILENCE_DETECTION constant
                    while silence_counter < SILENCE_DETECTION:
                        data = stream.read(
                            CHUNK)  # Read a new chunk from the stream
                        if LISTENING:
                            stream.write(data, CHUNK)
                        self.decoder_pipeline.process_data(data)

                        rms = audioop.rms(
                            data, 2
                        )  # Calculate Root Mean Square of current chunk again
                        if rms < THRESHOLD:  # If Root Mean Square value is less than THRESHOLD constant
                            silence_counter += 1  # Then increase silence counter
                        else:  # Else
                            silence_counter = 0  # Assign zero value to silence counter

                    stream.stop_stream()
                    self.decoder_pipeline.end_request()
                    while not self.finished:
                        time.sleep(0.1)
                    stream.start_stream()
                    words = self.words
                    words = [x for x in words if x != '<#s>']
                    com = ' '.join(words)
                    t = Thread(
                        target=VirtualAssistant.command, args=(com, args))
                    t.start()
                    self.reset()

                data = stream.read(CHUNK)  # Read a new chunk from the stream
                if LISTENING:
                    stream.write(data, CHUNK)

        except KeyboardInterrupt:
            stream.stop_stream()
            stream.close()
            p.terminate()
            self.loop.quit()
            raise KeyboardInterrupt


ERROR_HANDLER_FUNC = CFUNCTYPE(None, c_char_p, c_int, c_char_p, c_int,
                               c_char_p)


def py_error_handler(filename, line, function, err, fmt):
    pass


c_error_handler = ERROR_HANDLER_FUNC(py_error_handler)


@contextmanager
def noalsaerr():
    asound = cdll.LoadLibrary('libasound.so')
    asound.snd_lib_error_set_handler(c_error_handler)
    yield
    asound.snd_lib_error_set_handler(None)


if __name__ == '__main__':
    recognizer = KaldiRecognizer()
    recognizer.recognize()
