import unittest

from parameterized import parameterized

from mimicbot import filter

class TestFilter(unittest.TestCase):

    filter = None

    def __init__(self, *args, **kwargs):
        super(TestFilter, self).__init__(*args, **kwargs)
        self.filter = filter.Filter()

    def test_check_not_empty(self):
        func = self.filter.check_not_empty
        self.assertRaises(Exception, lambda: func(""))

    def test_check_too_long_pass(self):
        func = self.filter.check_too_long
        text = "a" * 140
        func(text)

    def test_check_too_long_fail(self):
        func = self.filter.check_too_long
        text = "a" * 141
        self.assertRaises(Exception, lambda: func(text))

    @parameterized.expand([
        "http",
        "https",
    ])
    def test_check_contains_link_pass(self, text):
        func = self.filter.check_contains_link
        func(text)

    @parameterized.expand([
        "http://example.com",
        "https://example.com",
    ])
    def test_check_contains_link_fail(self, text):
        func = self.filter.check_contains_link
        self.assertRaises(Exception, lambda: func(text))

    def test_check_contains_username_pass(self):
        func = self.filter.check_contains_username
        text = "@ username"
        func(text)

    def test_check_contains_username_fail(self):
        func = self.filter.check_contains_username
        text = "@username"
        self.assertRaises(Exception, lambda: funct(text))

    @parameterized.expand([
        "*action text*",
        "don't",
        "don’t",
        "\"double quotes\"",
        "'single quotes'",
        "'\"nested\" double quotes'",
        "\"'nested' single quotes\"",
        "“double curly quotes”",
        "‘single curly quotes’",
        "‘“nested” double curly quotes’",
        "“‘nested’ single curly quotes”",
        "(round braces)",
        "[square braces]",
        "{curly braces]}",
        "((nested) round brackets)",
        "[[nested] square brackets]",
        "{{nested} curly brackets}",
    ])
    def test_check_syntax_pass(self, text):
        func = self.filter.check_syntax
        func(text)

    @parameterized.expand([
        "*unbalanced action text",
        "don\"t",
        "don‘t",
        "don“t",
        "don”t",
        "\"unbalanced double quote",
        "'unbalanced single quote",
        "“unbalanced curly left double quote",
        "unbalanced curly right double quote”",
        "‘unbalanced curly left single quote",
        "unbalanced curly right single quote’",
        "(unbalanced opening round bracket",
        "unbalanced closing round bracket)",
        "[unbalanced opening square bracket",
        "unbalanced closing square bracket]",
        "{unbalanced opening curly bracket",
        "unbalanced closing curly bracket}",
        "((unbalanced nested opening round bracket)",
        "(unbalanced nested closing round bracket))",
        "[[unbalanced nested opening square bracket]",
        "[unbalanced nested closing square bracket]]",
        "{{unbalanced nested opening curly bracket}",
        "{unbalanced nested closing curly bracket}}",
    ])
    def test_check_syntax_fail(self, text):
        func = self.filter.check_syntax
        self.assertRaises(Exception, lambda: func(text))
