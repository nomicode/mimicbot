import unittest

import mimicbot

class TestGenerate(unittest.TestCase):

    def test_output_length(self):
        # simplistic
        for i in range(100):
            text = mimicbot.generate()
            self.assertTrue(len(text) > 0)

if __name__ == '__main__':
    unittest.main()

