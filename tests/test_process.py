import unittest

from parameterized import parameterized

import mimicbot

class TestProcess(unittest.TestCase):

    bot = None

    def __init__(self, *args, **kwargs):
        super(TestProcess, self).__init__(*args, **kwargs)
        self.bot = mimicbot.Bot("irlnomibot")

    @parameterized.expand([
        ("I LIKE TESTING", "I like testing"),
    ])
    def test_correct_case(self, input, expected):
        output = self.bot.processor.correct_case(input)
        self.assertEquals(output, expected)

    @parameterized.expand([
        ("test  ", "test"),
        ("  test  ", "test"),
        ("  test", "test"),
    ])
    def test_trim_spaces(self, input, expected):
        output = self.bot.processor.trim_spaces(input)
        self.assertEquals(output, expected)

    @parameterized.expand([
        ("test.", "test"),
        ("test....", "test...."),
        (".", "."),
    ])
    def test_trim_trailing_full_stop(self, input, expected):
        output = self.bot.processor.trim_trailing_full_stop(input)
        self.assertEquals(output, expected)

    @parameterized.expand([
        ("“test”", "\"test\""),
        ("‘test’", "'test'"),
    ])
    def test_replace_curly_quotes(self, input, expected):
        output = self.bot.processor.replace_curly_quotes(input)
        self.assertEquals(output, expected)

