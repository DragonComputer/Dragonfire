import os
import json

class ConfigDeepSpeech:

    def get_config(self, key):
        config = {}
        config['model'] = "/usr/share/dragonfire/deepspeech/models/output_graph.pb"
        config['alphabet'] = "/usr/share/dragonfire/deepspeech/models/alphabet.txt"
        config['lm'] = "/usr/share/dragonfire/deepspeech/models/lm.binary"
        config['trie'] = "/usr/share/dragonfire/deepspeech/models/trie"
        config['audiofiledir'] = "/usr/share/dragonfire/deepspeech/audio/"
        config['audiofilelength'] = "10"
        config['debug'] = "1"

        model = config['model']
        alphabet = config['alphabet']
        lm = config['lm']
        trie = config['trie']
        audiofiledir = config['audiofiledir']
        audiofilelength = config['audiofilelength']
        debug = config['debug']
        if key == 'model':
            return model
        elif key == 'alphabet':
            return alphabet
        elif key == 'lm':
            return lm
        elif key == 'trie':
            return trie
        elif key == 'audiofiledir':
            return audiofiledir
        elif key == 'audiofilelength':
            return audiofilelength
        elif key == 'debug':
            return debug
        else:
            raise Exception('Invalid key value.')
