import sys

import mimicbot
from mimicbot import twitter

def main(*args):
    bot = mimicbot.Bot()
    text = bot.get_text()
    print("finished\n")
    print(text)
    try:
        name = sys.argv[1]
        print(name)
        client = twitter.Client(name)
        client.post(text)
    except IndexError:
        pass

