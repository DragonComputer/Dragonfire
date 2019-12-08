#!/usr/bin/python3
# -*- coding: UTF-8 -*-

class UnknownSpeechRecognitionMode(Exception):
    def __init__(self, message = "", errors = None):
        super().__init__(message)
        self.errors = errors