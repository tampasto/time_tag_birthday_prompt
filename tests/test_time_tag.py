import unittest

from time_tag_birthday_prompt.time_tag import TimeTag, construct_time_tags

from time_tag_birthday_prompt.exceptions import (
    TimeTagErrorGroup, TimeFieldErrorGroup, IncorrectTimeFormatError,
    TimeDoesntExistError, TimeOrderError
    )


class TestTimeTag(unittest.TestCase):

    def testFirst(self):
        self.time_tag = TimeTag()
        self.assertEqual(1, 1)

if __name__ == '__main__':
    unittest.main()


class TestConstructTimeTags(unittest.TestCase):

    def testIncorrectDateFormatError(self):
        with self.assertRaises(TimeTagErrorGroup):
            self.birthday = construct_time_tags()
