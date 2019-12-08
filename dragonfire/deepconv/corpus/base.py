"""
Base class that contains common methods
"""

class CorpusBase:

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
                l = line[line.rindex("\t")+1:].strip()  # Strip metadata (timestamps, speaker names)

                lines.append({"text": l})

        return lines

    def getConversations(self):
        return self.conversations