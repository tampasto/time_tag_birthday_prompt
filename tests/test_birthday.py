from datetime import date
import unittest

from time_tag_birthday_prompt.birthday import Birthday

from .extend_unittest import assertGroupMatchesExceptions
from time_tag_birthday_prompt.exceptions import (
    BirthdayInitGroup, IncorrectParameterTypeError, IncorrectDateFormatError,
    NullYearError, DateDoesntExistError
    )


class TestBirthday__init__(unittest.TestCase):
    """Test `Birthday` object `__init__()` method."""

    def testParam_name_incorrectTypeInt(self):
        with self.assertRaises(BirthdayInitGroup) as cm:
            Birthday('2023-01-01', 123)
        assertGroupMatchesExceptions(
            self, cm.exception, [IncorrectParameterTypeError])

    def testParam_date_incorrectTypeTuple(self):
        with self.assertRaises(BirthdayInitGroup) as cm:
            Birthday((2023, 6, 13), 'name')
        assertGroupMatchesExceptions(
            self, cm.exception, [IncorrectParameterTypeError])

    def testParam_date_incorrectTypeDate(self):
        with self.assertRaises(BirthdayInitGroup) as cm:
            Birthday(date(2023, 6, 13), 'name')
        assertGroupMatchesExceptions(
            self, cm.exception, [IncorrectParameterTypeError])

    def testParam_date_IncorrectDateFormatError_noDate(self):
        with self.assertRaises(BirthdayInitGroup) as cm:
            Birthday('date_str', 'name')
        assertGroupMatchesExceptions(
            self, cm.exception, [IncorrectDateFormatError])

    def testParam_date_IncorrectDateFormatError_additinalParts(self):
        with self.assertRaises(BirthdayInitGroup) as cm:
            Birthday('2023-01-01-5', 'name')
        assertGroupMatchesExceptions(
            self, cm.exception, [IncorrectDateFormatError])

    def testParam_date_IncorrectDateFormatError_partNonNumeric(self):
        with self.assertRaises(BirthdayInitGroup) as cm:
            Birthday('2023-01-xx', 'name')
        assertGroupMatchesExceptions(
            self, cm.exception, [IncorrectDateFormatError])

    @unittest.expectedFailure
    def testParam_date_IncorrectDateFormatError_passNoZeroPadding(self):
        with self.assertRaises(BirthdayInitGroup) as cm:
            Birthday('2023-1-1', 'name')
        assertGroupMatchesExceptions(
            self, cm.exception, [IncorrectDateFormatError])

    def testParam_date_NullYearError(self):
        with self.assertRaises(BirthdayInitGroup) as cm:
            Birthday(f'{date.min.year}-01-01', 'name')
        assertGroupMatchesExceptions(
            self, cm.exception, [NullYearError])

    def testParam_date_DateDoesntExistError_monthOver(self):
        with self.assertRaises(BirthdayInitGroup) as cm:
            Birthday(f'2023-13-01', 'name')
        assertGroupMatchesExceptions(
            self, cm.exception, [DateDoesntExistError])

    def testParam_date_DateDoesntExistError_monthZero(self):
        with self.assertRaises(BirthdayInitGroup) as cm:
            Birthday(f'2023-00-01', 'name')
        assertGroupMatchesExceptions(
            self, cm.exception, [DateDoesntExistError])

    def testParam_date_DateDoesntExistError_dayOver(self):
        with self.assertRaises(BirthdayInitGroup) as cm:
            Birthday(f'2023-02-30', 'name')
        assertGroupMatchesExceptions(
            self, cm.exception, [DateDoesntExistError])

    def testParam_date_DateDoesntExistError_dayZero(self):
        with self.assertRaises(BirthdayInitGroup) as cm:
            Birthday(f'2023-02-00', 'name')
        assertGroupMatchesExceptions(
            self, cm.exception, [DateDoesntExistError])


if __name__ == '__main__':
    unittest.main()
