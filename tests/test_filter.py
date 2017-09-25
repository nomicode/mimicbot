import unittest

import mimicbot

from parameterized import parameterized

class TestFilter(unittest.TestCase):

    def test_141_chars_too_long(self):
        text = "a" * 140
        # if this fails it will raise an exception
        mimicbot.filter(text)
        text = "a" * 141
        self.assertRaises(Exception, lambda x: mimicbot.filter(text))

    @parameterized.expand([
        "http://example.com",
        "https://example.com",
    ])
    def test_links_not_ok(self, text):
        self.assertRaises(Exception, lambda x: mimicbot.filter(text))

if __name__ == '__main__':
    unittest.main()

