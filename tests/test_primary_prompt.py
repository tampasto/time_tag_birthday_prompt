from datetime import datetime, date
import unittest

from time_tag_birthday_prompt.primary_prompt import PrimaryPrompt

from time_tag_birthday_prompt.daily_prompt import DailyPrompt
from time_tag_birthday_prompt.exceptions import TimeTagErrorGroup, IncorrectReferenceError
from time_tag_birthday_prompt.time_tag import TimeTag, construct_time_tags


class TestPrimaryPrompt(unittest.TestCase):

    def testFirst(self):
        self.primary_prompt = PrimaryPrompt()
        self.assertEqual(1, 1)


if __name__ == '__main__':
    unittest.main()
