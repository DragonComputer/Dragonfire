# -*- coding: UTF-8 -*-

import unittest
from gi.repository import GObject, Gst
import thread
import logging
from decoder import DecoderPipeline
import time


class DecoderPipelineTests(unittest.TestCase):

    def __init__(self,  *args, **kwargs):
        super(DecoderPipelineTests, self).__init__(*args, **kwargs)
        logging.basicConfig(level=logging.INFO)

    @classmethod
    def setUpClass(cls):
            # voxforge/tri2b_mmi_b0.05 model:
            decoder_conf = {"model" : "models/english/final.mdl",
                            "lda-mat" : "models/english/final.mat",
                            "word-syms" : "models/english/words.txt",
                            "fst" : "models/english/HCLG.fst",
                            "silence-phones" : "6"}
            cls.decoder_pipeline = DecoderPipeline({"decoder" : decoder_conf})
            cls.words = []
            cls.finished = False

            cls.decoder_pipeline.set_word_handler(cls.word_getter)
            cls.decoder_pipeline.set_eos_handler(cls.set_finished, cls.finished)

            loop = GObject.MainLoop()
            thread.start_new_thread(loop.run, ())

    @classmethod
    def word_getter(cls, word):
        cls.words.append(word)

    @classmethod
    def set_finished(cls, finished):
        cls.finished = True

    def setUp(self):
        self.__class__.words = []
        self.__class__.finished = False



    def testWav(self):
        self.decoder_pipeline.init_request("testWav", "")
        f = open("tests/ten_digits.wav", "rb")
        for block in iter(lambda: f.read(16000*2*2/4), ""):
            time.sleep(0.25)
            self.decoder_pipeline.process_data(block)

        self.decoder_pipeline.end_request()


        while not self.finished:
            time.sleep(1)
        self.assertEqual(['ONE', 'TWO', 'THREE', 'FOUR', 'FIVE', 'SIX', 'SEVEN', 'EIGHT', '<#s>'], self.words)



def main():
    unittest.main()

if __name__ == '__main__':
    main()
