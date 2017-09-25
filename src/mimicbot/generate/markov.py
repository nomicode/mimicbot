import os.path
import random
import re

from MarkovText import MarkovText

class MarkovGenerator:

    chain = None

    def __init__(self):
        self.chain = MarkovText.Markov()
        filename = os.path.expanduser("~/.mimicbot/irlnomi/tweets.txt" % name)
        self.chain.add_to_dict(open(filename).read())

    def run(self):
        sentence_count = random.randint(1, 6)
        return self.chain.create_sentences(sentence_count)

