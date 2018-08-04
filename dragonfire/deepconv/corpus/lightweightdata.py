import os

"""
Load data from a dataset of simply-formatted data

from A to B
from B to A
from A to B
from B to A
from A to B
===
from C to D
from D to C
from C to D
from D to C
from C to D
from D to C
...

`===` lines just separate linear conversations between 2 people.

"""

class LightweightData:
    """
    """

    def __init__(self, lightweightFile):
        """
        Args:
            lightweightFile (string): file containing our lightweight-formatted corpus
        """
        self.CONVERSATION_SEP = "==="
        self.conversations = []
        self.loadLines(lightweightFile + '.txt')

    def loadLines(self, fileName):
        """
        Args:
            fileName (str): file to load
        """

        linesBuffer = []
        with open(fileName, 'r') as f:
            for line in f:
                l = line.strip()
                if l == self.CONVERSATION_SEP:
                    self.conversations.append({"lines": linesBuffer})
                    linesBuffer = []
                else:
                    linesBuffer.append({"text": l})
            if len(linesBuffer):  # Eventually flush the last conversation
                self.conversations.append({"lines": linesBuffer})

    def getConversations(self):
        return self.conversations
