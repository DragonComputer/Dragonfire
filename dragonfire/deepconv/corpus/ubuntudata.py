import os

from tqdm import tqdm

from dragonfire.deepconv.corpus.base import CorpusBase

"""
Ubuntu Dialogue Corpus

http://arxiv.org/abs/1506.08909

"""

class UbuntuData(CorpusBase):
    """
    """

    def __init__(self, dirName):
        """
        Args:
            dirName (string): directory where to load the corpus
        """
        super().__init__(dirName)

        self.MAX_NUMBER_SUBDIR = 10
        self.conversations = []
        __dir = os.path.join(dirName, "dialogs")
        number_subdir = 0
        for sub in tqdm(os.scandir(__dir), desc="Ubuntu dialogs subfolders", total=len(os.listdir(__dir))):
            if number_subdir == self.MAX_NUMBER_SUBDIR:
                print("WARNING: Early stoping, only extracting {} directories".format(self.MAX_NUMBER_SUBDIR))
                return

            if sub.is_dir():
                number_subdir += 1
                for f in os.scandir(sub.path):
                    if f.name.endswith(".tsv"):
                        self.conversations.append({"lines": self.loadLines(f.path)})
