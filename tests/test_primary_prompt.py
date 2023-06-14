from datetime import datetime, date
import unittest

from time_tag_birthday_prompt.primary_prompt import PrimaryPrompt

from time_tag_birthday_prompt.daily_prompt import DailyPrompt
from time_tag_birthday_prompt.exceptions import (
    TimeTagErrorGroup, IncorrectParameterTypeError, LineWidthLessThanOneError)
from time_tag_birthday_prompt.time_tag import TimeTag, construct_time_tags

TDAY = 2023, 6, 10


class TestPrimaryPromptInit(unittest.TestCase):
    """Test `DailyPrompt` object `__init__()` method."""

    @unittest.expectedFailure
    def testCorrectParameterTypeDailyPromptObject(self):
        with self.assertRaises(IncorrectParameterTypeError):
            PrimaryPrompt(daily_prompt=DailyPrompt())

    @unittest.expectedFailure
    def testCorrectParameterTypeDailyPromptNone(self):
        with self.assertRaises(IncorrectParameterTypeError):
            PrimaryPrompt(daily_prompt=None)

    def testIncorrectParameterTypeErrorDailyPromptStr(self):
        with self.assertRaises(IncorrectParameterTypeError):
            PrimaryPrompt(daily_prompt='daily_prompt')

    def testIncorrectParameterTypeErrorDefaultPrompt(self):
        with self.assertRaises(IncorrectParameterTypeError):
            PrimaryPrompt(daily_prompt=DailyPrompt(), default_prompt=-1)

    def testIncorrectParameterTypeErrorTagEndPrompt(self):
        with self.assertRaises(IncorrectParameterTypeError):
            PrimaryPrompt(daily_prompt=DailyPrompt(), tag_end_prompt=-1)

    def testIncorrectParameterTypeErrorLineWidth(self):
        with self.assertRaises(IncorrectParameterTypeError):
            PrimaryPrompt(daily_prompt=DailyPrompt(), line_width=None)

    def testIncorrectParameterTypeErrorDailyPromptOnInit(self):
        with self.assertRaises(IncorrectParameterTypeError):
            PrimaryPrompt(daily_prompt=DailyPrompt(), daily_prompt_on_init='False')

    def testLineWidthLessThanOneErrorZero(self):
        with self.assertRaises(LineWidthLessThanOneError):
            PrimaryPrompt(daily_prompt=DailyPrompt(), line_width=0)

    def testLineWidthLessThanOneErrorMinusOne(self):
        with self.assertRaises(LineWidthLessThanOneError):
            PrimaryPrompt(daily_prompt=DailyPrompt(), line_width=-1)


class TestPrimaryPromptGetStr(unittest.TestCase):
    """Test `PrimaryPrompt` object `__str__()` method."""

    def testDailyPromptPrints(self):
        primary_prompt_a = PrimaryPrompt(daily_prompt=DailyPrompt())
        primary_prompt_b = PrimaryPrompt(daily_prompt=None)
        self.assertNotEqual(len(str(primary_prompt_a)), len(str(primary_prompt_b)))

    def testTagJustBefore(self):
        primary_prompt = PrimaryPrompt(default_prompt='>>> ', tag_end_prompt='> ')
        str(primary_prompt)
        primary_prompt.time_tags = [
            TimeTag('09:00', '15:00', 'text')
            ]
        self.assertEqual(primary_prompt.get_str(datetime(*TDAY, 8, 59)), '>>> ')

    def testTagStartTime(self):
        primary_prompt = PrimaryPrompt(default_prompt='>>> ', tag_end_prompt='> ')
        str(primary_prompt)
        primary_prompt.time_tags = [
            TimeTag('09:00', '15:00', 'text')
            ]
        self.assertEqual(primary_prompt.get_str(datetime(*TDAY, 9, 0)), 'text> ')

    def testTagJustBeforeStop(self):
        primary_prompt = PrimaryPrompt(default_prompt='>>> ', tag_end_prompt='> ')
        str(primary_prompt)
        primary_prompt.time_tags = [
            TimeTag('09:00', '15:00', 'text')
            ]
        self.assertEqual(primary_prompt.get_str(datetime(*TDAY, 14, 59)), 'text> ')

    def testTagStopTime(self):
        primary_prompt = PrimaryPrompt(default_prompt='>>> ', tag_end_prompt='> ')
        str(primary_prompt)
        primary_prompt.time_tags = [
            TimeTag('09:00', '15:00', 'text')
            ]
        self.assertEqual(primary_prompt.get_str(datetime(*TDAY, 15, 0)), '>>> ')

    def testTagEndAtMidnightJustBefore(self):
        primary_prompt = PrimaryPrompt(default_prompt='>>> ', tag_end_prompt='> ')
        str(primary_prompt)
        primary_prompt.time_tags = [
            TimeTag('09:00', '00:00', 'text')
            ]
        self.assertEqual(primary_prompt.get_str(datetime(*TDAY, 23, 59)), 'text> ')

    def testTagEndAtMidnightAtMidnight(self):
        primary_prompt = PrimaryPrompt(default_prompt='>>> ', tag_end_prompt='> ')
        str(primary_prompt)
        primary_prompt.time_tags = [
            TimeTag('09:00', '00:00', 'text')
            ]
        self.assertEqual(primary_prompt.get_str(datetime(*TDAY, 0, 0)), '>>> ')

    def testTagStartAtMidnightJustBefore(self):
        primary_prompt = PrimaryPrompt(default_prompt='>>> ', tag_end_prompt='> ')
        str(primary_prompt)
        primary_prompt.time_tags = [
            TimeTag('00:00', '15:00', 'text')
            ]
        self.assertEqual(primary_prompt.get_str(datetime(*TDAY, 23, 59)), '>>> ')

    def testTagStartAtMidnightAtMidnight(self):
        primary_prompt = PrimaryPrompt(default_prompt='>>> ', tag_end_prompt='> ')
        str(primary_prompt)
        primary_prompt.time_tags = [
            TimeTag('00:00', '15:00', 'text')
            ]
        self.assertEqual(primary_prompt.get_str(datetime(*TDAY, 0, 0)), 'text> ')

    def testTagOverlapPrecedingStartsFirst(self):
        primary_prompt = PrimaryPrompt(default_prompt='>>> ', tag_end_prompt='> ')
        str(primary_prompt)
        primary_prompt.time_tags = [
            TimeTag('09:00', '15:00', 'text'),
            TimeTag('14:00', '15:00', 'str')
            ]
        self.assertEqual(primary_prompt.get_str(datetime(*TDAY, 14, 30)), 'str> ')

    def testTagOverlapLatterStartsFirst(self):
        primary_prompt = PrimaryPrompt(default_prompt='>>> ', tag_end_prompt='> ')
        str(primary_prompt)
        primary_prompt.time_tags = [
            TimeTag('14:00', '15:00', 'text'),
            TimeTag('09:00', '15:00', 'str')
            ]
        self.assertEqual(primary_prompt.get_str(datetime(*TDAY, 14, 30)), 'str> ')

    def testTagOverlapMidJustBefore(self):
        primary_prompt = PrimaryPrompt(default_prompt='>>> ', tag_end_prompt='> ')
        str(primary_prompt)
        primary_prompt.time_tags = [
            TimeTag('09:00', '15:00', 'text'),
            TimeTag('14:00', '15:00', 'str')
            ]
        self.assertEqual(primary_prompt.get_str(datetime(*TDAY, 13, 59)), 'text> ')

    def testTagOverlapMidJustAfter(self):
        primary_prompt = PrimaryPrompt(default_prompt='>>> ', tag_end_prompt='> ')
        str(primary_prompt)
        primary_prompt.time_tags = [
            TimeTag('09:00', '15:00', 'text'),
            TimeTag('14:00', '15:00', 'str')
            ]
        self.assertEqual(primary_prompt.get_str(datetime(*TDAY, 14, 0)), 'str> ')

    def testTagOverlapEndJustBefore(self):
        primary_prompt = PrimaryPrompt(default_prompt='>>> ', tag_end_prompt='> ')
        str(primary_prompt)
        primary_prompt.time_tags = [
            TimeTag('09:00', '15:00', 'text'),
            TimeTag('14:00', '16:00', 'str')
            ]
        self.assertEqual(primary_prompt.get_str(datetime(*TDAY, 14, 59)), 'str> ')

    def testTagOverlapEndJustAfter(self):
        primary_prompt = PrimaryPrompt(default_prompt='>>> ', tag_end_prompt='> ')
        str(primary_prompt)
        primary_prompt.time_tags = [
            TimeTag('09:00', '15:00', 'text'),
            TimeTag('14:00', '16:00', 'str')
            ]
        self.assertEqual(primary_prompt.get_str(datetime(*TDAY, 15, 0)), 'str> ')

    def testTagOverlapBoundaryJustBefore(self):
        primary_prompt = PrimaryPrompt(default_prompt='>>> ', tag_end_prompt='> ')
        str(primary_prompt)
        primary_prompt.time_tags = [
            TimeTag('09:00', '11:00', 'text'),
            TimeTag('11:00', '15:00', 'str')
            ]
        self.assertEqual(primary_prompt.get_str(datetime(*TDAY, 10, 59)), 'text> ')

    def testTagOverlapBoundaryJustAfter(self):
        primary_prompt = PrimaryPrompt(default_prompt='>>> ', tag_end_prompt='> ')
        str(primary_prompt)
        primary_prompt.time_tags = [
            TimeTag('09:00', '11:00', 'text'),
            TimeTag('11:00', '15:00', 'str')
            ]
        self.assertEqual(primary_prompt.get_str(datetime(*TDAY, 11, 0)), 'str> ')


if __name__ == '__main__':
    unittest.main()
