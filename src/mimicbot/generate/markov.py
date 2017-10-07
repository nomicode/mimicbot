import os
import random
import re
import csv
import html

from MarkovText import MarkovText

from whoosh import fields, index, qparser

class MarkovGenerator:

    dir = None

    index = None

    chain = None

    def __init__(self, dir):
        self.dir = dir

    def get_index(self):
        schema = fields.Schema(content=fields.TEXT)
        index_dir = os.path.join(self.dir, "index")
        if os.path.exists(index_dir):
            self.index = index.open_dir(index_dir)
        else:
            os.mkdir(index_dir)
            self.index = index.create_in(index_dir, schema)

    def search(self):
        self.get_index()
        with self.index.searcher() as searcher:
            print("hi")
            parser = qparser.QueryParser("content", self.index.schema)
            query = parser.parse("*")
            results = searcher.search(query, limit=100)
            for result in results:
                print(result)

    def read_csv(self, filename):
        with open(filename, "r") as csv_file:
            reader = csv.reader(csv_file, delimiter=",", quotechar="\"")
            for row in reader:
                text = html.unescape(row[5])
                yield text

    def train_csv(self, filename):
        self.get_index()
        writer = self.index.writer()
        for text in self.read_csv(filename):
            writer.add_document(content=text)
        writer.commit()

    def run(self):
        print("foo")
        self.search()
        return
        self.chain = MarkovText.Markov()
        filename = os.path.expanduser("~/.mimicbot/%s/tweets.txt" % name)
        self.chain.add_to_dict(open(filename).read())
        sentence_count = random.randint(1, 6)
        return self.chain.create_sentences(sentence_count)

