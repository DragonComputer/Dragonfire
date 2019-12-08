import os

from dragonfire.deepconv.corpus.base import CorpusBase

"""
Load transcripts from the Supreme Court of the USA.

Available from here:
https://github.com/pender/chatbot-rnn

"""

class ScotusData(CorpusBase):
    """
    """

    def __init__(self, dirName):
        """
        Args:
            dirName (string): directory where to load the corpus
        """
        super().__init__(dirName)

        self.lines = self.loadLines(os.path.join(dirName, "scotus"))
        self.conversations = [{"lines": self.lines}]
