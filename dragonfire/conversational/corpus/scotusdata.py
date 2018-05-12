import os

"""
Load transcripts from the Supreme Court of the USA.

Available from here:
https://github.com/pender/chatbot-rnn

"""

class ScotusData:
    """
    """

    def __init__(self, dirName):
        """
        Args:
            dirName (string): directory where to load the corpus
        """
        self.lines = self.loadLines(os.path.join(dirName, "scotus"))
        self.conversations = [{"lines": self.lines}]


    def loadLines(self, fileName):
        """
        Args:
            fileName (str): file to load
        Return:
            list<dict<str>>: the extracted fields for each line
        """
        lines = []

        with open(fileName, 'r') as f:
            for line in f:
                l = line[line.index(":")+1:].strip()  # Strip name of speaker.

                lines.append({"text": l})

        return lines


    def getConversations(self):
        return self.conversations
