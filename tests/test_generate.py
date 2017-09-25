import unittest

from mimicbot import generate

class TestGenerate(unittest.TestCase):

    generator = None

    def __init__(self, *args, **kwargs):
        super(TestGenerate, self).__init__(*args, **kwargs)
        self.generator = generate.Generator()

    def test_output_length(self):
        # simplistic
        for i in range(100):
            text = self.generator.run()
            self.assertTrue(len(text) > 0)
