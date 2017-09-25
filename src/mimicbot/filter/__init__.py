import re

class Filter:

    def run(self, text):
        if len(text) > 140:
            raise Exception("too long")
        if re.findall("http(s?)://", text):
            raise Exception("contains link")
        return text

# import language_check

# tool = language_check.LanguageTool('en-GB')

# print(text)
# matches = tool.check(text)
# text = language_check.correct(text, matches)
