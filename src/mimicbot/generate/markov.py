import os
import random
import re
import csv
import html

import dateutil
from dateutil import parser

from MarkovText import MarkovText

# TODO: don't use them like this
from whoosh import fields, index, qparser, analysis, sorting
import whoosh.query

import pprint
pp = pprint.PrettyPrinter(indent=4, depth=9)

class MarkovGenerator:

    dir = None

    index = None

    chain = None

    context = None

    def __init__(self, dir):
        self.dir = dir

    def get_index(self):
        stem_ana = analysis.StemmingAnalyzer()
        schema = fields.Schema(
            id=fields.ID(unique=True),
            datetime=fields.DATETIME(sortable=True),
            reply=fields.BOOLEAN,
            retweet=fields.BOOLEAN,
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
            keywords = searcher.key_terms_from_text("text", query, numterms=20)
            keyword_query = " ".join(
                [keyword for keyword, score in keywords])

            print("keyword query: %s" % keyword_query)

            parser = qparser.QueryParser(
                "text", self.index.schema, group=qparser.OrGroup)
            query = parser.parse(keyword_query)

            restrict_retweets = whoosh.query.Term("retweet", True)

            results = searcher.search(query, mask=restrict_retweets, limit=100)
            for result in results:
                yield result["text"]

    def get_context(self, number=5):
        if self.context:
            return self.context

        self.get_index()

        from whoosh.qparser.dateparse import DateParserPlugin

        print("running date query...")
        datetimes = sorting.FieldFacet("datetime", reverse=True)
        parser = qparser.QueryParser("text", self.index.schema)
        query = parser.parse("*")
        searcher = self.index.searcher()

        restrict_replies = whoosh.query.Term("reply", True)

        results = searcher.search(
            query, mask=restrict_replies, sortedby=datetimes, limit=number)

        self.context = ""
        for result in results:
            print("context add: %s" % result["text"])
            self.context += result["text"]

        print("combined context: %s" % self.context)

        import re

        # don't want these influence context
        # drop usernames
        self.context = re.sub(r"@[^ ]+", " ", self.context)
        # drop links
        self.context = re.sub(r"http(s?)://[^ ]+", " ", self.context)
        # drop cut-off text from the end of manual rts
        self.context = re.sub(r"[^ ]+…$", " ", self.context)

        print("filtered context: %s" % self.context)

        return self.context

    def read_csv(self, filename):
        with open(filename, "r") as csv_file:
            reader = csv.reader(csv_file, delimiter=",", quotechar="\"")
            for row in reader:
                if row[0] == "tweet_id":
                    # skip header row
                    continue
                id = row[0]
                datetime = dateutil.parser.parse(row[3])
                reply = True if row[1] else False
                retweet = True if row[6] else False
                text = html.unescape(row[5])
                yield id, datetime, reply, retweet, text

    def train_csv(self, filename):
        self.get_index()
        writer = self.index.writer()
        for id, datetime, reply, retweet, text in self.read_csv(filename):
            print("writing doc: %s, %s, %s, %s, %s" % (id, datetime, reply, retweet, text))
            writer.update_document(id=id, datetime=datetime, reply=reply, retweet=retweet, text=text)
        writer.commit()
        doc_count = self.index.doc_count()
        print("doc count: %s" % doc_count)

    def train_latest_tweets(self, tweets):
        # TODO: fix duplication with train_csv method
        self.get_index()
        writer = self.index.writer()
        for tweet in tweets:
            id = tweet["id_str"]
            datetime = dateutil.parser.parse(tweet["created_at"])
            reply = True if tweet["in_reply_to_status_id"] else False
            retweet = True if tweet["retweeted"] else False
            text = html.unescape(tweet["text"])
            print("writing doc: %s, %s, %s, %s, %s" % (id, datetime, reply, retweet, text))
            writer.update_document(id=id, datetime=datetime, reply=reply, retweet=retweet, text=text)
        writer.commit()
        doc_count = self.index.doc_count()
        print("doc count: %s" % doc_count)

    def run(self, use_context, manual_context):
        # TODO needs to progressively search if we're not turning up enough
        # results
        print("run")
        context = ""
        if use_context:
            context = self.get_context()
        if manual_context:
            context = manual_context
        print("searching...")
        results = list(self.search(context))
        print("got %s results" % len(results))
        self.chain = MarkovText.Markov()
        for result in results:
            self.chain.add_to_dict(result)
        sentence_count = random.randint(1, 6)
        return self.chain.create_sentences(sentence_count)

