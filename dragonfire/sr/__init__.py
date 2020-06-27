#!/usr/bin/python3
# -*- coding: UTF-8 -*-

from __future__ import absolute_import

# Operates on sound fragments consisting of signed integer samples 8, 16
# or 32 bits wide, stored in Python strings.
import audioop
from contextlib import contextmanager
from ctypes import CFUNCTYPE, c_char_p, c_int, cdll
from threading import Thread

import speech_recognition as sr
import pyaudio  # Provides Python bindings for PortAudio, the cross platform audio API
from dragonfire import VirtualAssistant
import deepspeech
from dragonfire.sr.exceptions import UnknownSpeechRecognitionMode
import numpy as np

CHUNK = 8000  # Smallest unit of audio. 1024 bytes
FORMAT = pyaudio.paInt16  # Data format
CHANNELS = 1  # Number of channels
RATE = 16000  # Bit Rate of audio stream / Frame Rate
THRESHOLD = 1000  # Threshhold value for detecting stimulant
LISTENING = False

DEEPSPEECH_MODEL = '/usr/share/dragonfire/deepspeech/models/deepspeech-0.7.4-models.pbmm'
DEEPSPEECH_SCORER = '/usr/share/dragonfire/deepspeech/models/deepspeech-0.7.4-models.scorer'

class SpeechRecognizer():
    def __init__(self, mode):
        # logging.basicConfig(level=logging.INFO)
        self.__class__.finished = False

        self.modes = ["deepspeech", 'gspeech']
        if mode not in self.modes:
            raise UnknownSpeechRecognitionMode();
        else:
            self.mode = mode

        if self.mode == 'gspeech':
            self.silence_detection = 3
            self.recognizer = sr.Recognizer()
        else:
            self.recognizer = deepspeech.Model(DEEPSPEECH_MODEL)
            self.recognizer.enableExternalScorer(DEEPSPEECH_SCORER)
            self.silence_detection = 1

    @classmethod
    def set_finished(cls, finished):
        cls.finished = finished

    def reset(self):
        self.__class__.finished = False

    def recognize(self, her):

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
            data = stream.read(CHUNK)  # Get first data frame from the microphone
            # Loop over the frames of the audio / data chunks
            audio = None
            # print("START LISTENNING")
            while data != '':
                rms = audioop.rms(data, 2)  # Calculate Root Mean Square of current chunk
                if rms >= THRESHOLD:  # If Root Mean Square value is greater than THRESHOLD constant
                    audio = data
                    silence_counter = 0  # Define silence counter
                    # While silence counter value less than SILENCE_DETECTION constant
                    while silence_counter < self.silence_detection:
                        data = stream.read(CHUNK)  # Read a new chunk from the stream
                        if LISTENING:
                            stream.write(data, CHUNK)
                        audio = audio + data

                        rms = audioop.rms(data, 2)  # Calculate Root Mean Square of current chunk again
                        if rms < THRESHOLD:  # If Root Mean Square value is less than THRESHOLD constant
                            silence_counter += 1  # Then increase silence counter
                        else:  # Else
                            silence_counter = 0  # Assign zero value to silence counter

                    # print("Analyzing...")
                    stream.stop_stream()

                    if self.mode == 'deepspeech':
                        audio = np.fromstring(audio, dtype=np.int16)  # Fix data type
                        #com = SpeechServerMain.ds.stt(audio, RATE)
                        stream_context = self.recognizer.createStream()
                        stream_context.feedAudioContent(audio)
                        com = stream_context.finishStream()
                        stream.start_stream()
                        # print(com)
                        t = Thread(target=her.command, args=(com,))
                        t.start()
                    elif self.mode == 'gspeech':
                        audio_data = sr.AudioData(audio, RATE, p.get_sample_size(FORMAT))
                        try:
                            com = self.recognizer.recognize_google(audio_data)
                            print(com)
                            t = Thread(target=her.command, args=(com,))
                            t.start()
                        except sr.UnknownValueError:
                            # print("Google Speech Recognition could not understand audio")
                            pass
                        except sr.RequestError as e:
                            print("Could not request results from Google Speech Recognition service; {0}".format(e))

                        stream.start_stream()
                    else:
                        break

                    self.reset()

                data = stream.read(CHUNK)  # Read a new chunk from the stream
                if LISTENING:
                    stream.write(data, CHUNK)

        except KeyboardInterrupt:
            stream.stop_stream()
            stream.close()
            p.terminate()
            # self.loop.quit()
            raise KeyboardInterrupt


ERROR_HANDLER_FUNC = CFUNCTYPE(None, c_char_p, c_int, c_char_p, c_int, c_char_p)


def py_error_handler(filename, line, function, err, fmt):
    pass


c_error_handler = ERROR_HANDLER_FUNC(py_error_handler)


@contextmanager
def noalsaerr():
    asound = cdll.LoadLibrary('libasound.so')
    asound.snd_lib_error_set_handler(c_error_handler)
    yield
    asound.snd_lib_error_set_handler(None)
