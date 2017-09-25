import sys

import mimicbot
from mimicbot import twitter

def main(*args):
    name = sys.argv[1]
    bot = mimicbot.Bot(name)
    text = bot.get_text()
    print("finished\n")
    print(text)
    try:
        post = sys.argv[2]
        client = twitter.Client(name)
        client.post(text)
    except IndexError:
        pass

