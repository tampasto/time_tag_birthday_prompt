from datetime import datetime
import unittest

from time_tag_birthday_prompt.secondary_prompt import SecondaryPrompt

from time_tag_birthday_prompt.exceptions import IncorrectReferenceError
from time_tag_birthday_prompt.primary_prompt import PrimaryPrompt


class TestSecondaryPrompt(unittest.TestCase):

    def testFirst(self):
        self.secondary_prompt = SecondaryPrompt()
        self.assertEqual(1, 1)


if __name__ == '__main__':
    unittest.main()
