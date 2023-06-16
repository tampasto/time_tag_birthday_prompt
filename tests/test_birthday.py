from datetime import date
import unittest

from time_tag_birthday_prompt.birthday import Birthday

from time_tag_birthday_prompt.exceptions import (
    ConstructBirthdaysGroup, IncorrectParameterTypeError, IncorrectDateFormatError,
    NullYearError, DateDoesntExistError
    )


class TestBirthdayInit(unittest.TestCase):
    """Test `Birthday` object `__init__()` method."""

    def testIncorrectDateTypeError(self):
        with self.assertRaises(IncorrectParameterTypeError):
            Birthday((2023, 6, 13), 'name')

    @unittest.expectedFailure
    def testIncorrectDateTypeError(self):
        with self.assertRaises(IncorrectParameterTypeError):
            Birthday(date(2023, 6, 13), 'name')

    def testIncorrectNameTypeError(self):
        with self.assertRaises(IncorrectParameterTypeError):
            Birthday('2023-01-01', 123)

    def testIncorrectDateFormatErrorNoDate(self):
        with self.assertRaises(IncorrectDateFormatError):
            Birthday('date_str', 'name')

    def testIncorrectDateFormatErrorAdditinalParts(self):
        with self.assertRaises(IncorrectDateFormatError):
            Birthday('2023-01-01-5', 'name')

    def testIncorrectDateFormatErrorPartNonNumeric(self):
        with self.assertRaises(IncorrectDateFormatError):
            Birthday('2023-01-xx', 'name')

    @unittest.expectedFailure
    def testIncorrectDateFormatPassNoZeroPadding(self):
        with self.assertRaises(IncorrectDateFormatError):
            Birthday('2023-1-1', 'name')

    def testNullYearError(self):
        with self.assertRaises(NullYearError):
            Birthday(f'{date.min.year}-01-01', 'name')

    def testDateDoesntExistErrorMonthOver(self):
        with self.assertRaises(DateDoesntExistError):
            Birthday(f'2023-13-01', 'name')

    def testDateDoesntExistErrorMonthZero(self):
        with self.assertRaises(DateDoesntExistError):
            Birthday(f'2023-00-01', 'name')

    def testDateDoesntExistErrorDayOver(self):
        with self.assertRaises(DateDoesntExistError):
            Birthday(f'2023-02-30', 'name')

    def testDateDoesntExistErrorDayZero(self):
        with self.assertRaises(DateDoesntExistError):
            Birthday(f'2023-02-00', 'name')


if __name__ == '__main__':
    unittest.main()
