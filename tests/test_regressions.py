import unittest

from parameterized import parameterized

import mimicbot

class TestRegressions(unittest.TestCase):

    bot = None

    def __init__(self, *args, **kwargs):
        super(TestRegressions, self).__init__(*args, **kwargs)
        self.bot = mimicbot.Bot("irlnomibot")

    @parameterized.expand([
        "picard “space"
    ])
    def test_regression_bad_syntax(self, text):
        func = self.bot._handle
        error_str = None
        try:
            func(text)
        except Exception as error:
            error_str = str(error)
        self.assertEquals(error_str, "bad syntax")
