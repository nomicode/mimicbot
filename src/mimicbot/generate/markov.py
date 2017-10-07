import os
import random
import re
import csv
import html

import dateutil
from dateutil import parser

from MarkovText import MarkovText

from whoosh import fields, index, qparser, analysis

class MarkovGenerator:

    dir = None

    index = None

    chain = None

    def __init__(self, dir):
        self.dir = dir

    def get_index(self):
        stem_ana = analysis.StemmingAnalyzer()
        schema = fields.Schema(
            id=fields.ID(unique=True),
            datetime=fields.DATETIME,
            text=fields.TEXT(analyzer=stem_ana, stored=True)
        )
        index_dir = os.path.join(self.dir, "index")
        if os.path.exists(index_dir):
            self.index = index.open_dir(index_dir)
        else:
            os.mkdir(index_dir)
            self.index = index.create_in(index_dir, schema)

    def search(self, query):
        self.get_index()

        import pprint
        pp = pprint.PrettyPrinter(indent=4, depth=9)


        with self.index.searcher() as searcher:
            # improve relevance! form query from keywords
            keywords = searcher.key_terms_from_text("text", query)
            keyword_query = " ".join(
                [keyword for keyword, score in keywords])

            print("keyword query: %s" % keyword_query)

            parser = qparser.QueryParser(
                "text", self.index.schema, group=qparser.OrGroup)
            query = parser.parse(keyword_query)
            results = searcher.search(query, limit=100)
            for result in results:
                yield result["text"]

    def read_csv(self, filename):
        import pprint
        pp = pprint.PrettyPrinter(indent=4, depth=9)

        with open(filename, "r") as csv_file:
            reader = csv.reader(csv_file, delimiter=",", quotechar="\"")
            for row in reader:
                if row[0] == "tweet_id":
                    # skip header row
                    continue
                id = row[0]
                datetime = dt = dateutil.parser.parse(row[3])
                text = html.unescape(row[5])
                yield id, datetime, text

    def train_csv(self, filename):
        self.get_index()
        writer = self.index.writer()
        for id, datetime, text in self.read_csv(filename):
            print("writing doc: %s, %s, %s" % (id, datetime, text))
            writer.update_document(id=id, datetime=datetime, text=text)
        writer.commit()
        doc_count = self.index.doc_count()
        print("doc count: %s" % doc_count)

    def train_latest_tweets(self, tweets):
        import pprint
        pp = pprint.PrettyPrinter(indent=4, depth=9)
        pp.pprint(tweets)

    def run(self, manual_context):
        print("run")
        results = list(self.search(manual_context))
        print("got %s results" % len(results))
        self.chain = MarkovText.Markov()
        for result in results:
            self.chain.add_to_dict(result)
        sentence_count = random.randint(1, 6)
        return self.chain.create_sentences(sentence_count)

