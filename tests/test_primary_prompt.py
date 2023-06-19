from datetime import datetime
from tempfile import TemporaryFile
from typing import Tuple
import unittest

from time_tag_birthday_prompt.primary_prompt import PrimaryPrompt

from time_tag_birthday_prompt.data_loader import DataLoader
from time_tag_birthday_prompt.exceptions import (
    BirthdayNotifyDaysLessThanZeroError, IncorrectParameterTypeError,
    LineWidthLessThanTenError
    )
from time_tag_birthday_prompt.time_tag import TimeTag

TDAY = 2023, 6, 10


class TestPrimaryPrompt__init__(unittest.TestCase):
    """Test `PrimaryPrompt` object `__init__()` method."""

    def testParam_birthday_notify_days_incorrectType(self):
        with self.assertRaises(IncorrectParameterTypeError):
            PrimaryPrompt(birthday_notify_days=(5, 6))
    
    def testParam_birthday_notify_days_BirthdayNotifyDaysLessThanZeroError_minusOne(self):
        with self.assertRaises(BirthdayNotifyDaysLessThanZeroError):
            PrimaryPrompt(birthday_notify_days=-1)

    def testParam_default_prompt_incorrectType(self):
        with self.assertRaises(IncorrectParameterTypeError):
            PrimaryPrompt(default_prompt=-1)

    def testParam_tag_end_prompt_incorrectType(self):
        with self.assertRaises(IncorrectParameterTypeError):
            PrimaryPrompt(tag_end_prompt=-1)

    def testParam_line_width_incorrectType(self):
        with self.assertRaises(IncorrectParameterTypeError):
            PrimaryPrompt(line_width=None)

    def testParam_line_width_LineWidthLessThanOneError_nine(self):
        with self.assertRaises(LineWidthLessThanTenError):
            PrimaryPrompt(line_width=9)

    def testParam_line_width_LineWidthLessThanOneError_minusOne(self):
        with self.assertRaises(LineWidthLessThanTenError):
            PrimaryPrompt(line_width=-1)


class TestPrimaryPrompt_get_str(unittest.TestCase):
    """Test `PrimaryPrompt` object `get_str()` method."""

    def testPrologMessages(self):
        pass

    def testPrologBirthdayNotifier(self):
        pass


class TestPrimaryPrompt_get_prompt(unittest.TestCase):
    """Test `PrimaryPrompt` object `get_prompt()` method."""

    def assertPromptEqual(
            self, expect: str, time: Tuple[int, int], json: str,
            default_prompt: str = '>>> ', tag_end_prompt: str = '> '):
        dl = None
        with TemporaryFile(mode='w+', encoding='utf-8') as tf:
            tf.write('{"timeTags": [' + json + '], "birthdays": null}')
            tf.seek(0)
            dl = DataLoader(tf, '<testing>')
        pp = PrimaryPrompt(
            default_prompt=default_prompt,
            tag_end_prompt=tag_end_prompt,
            data_loader=dl
            )
        self.assertEqual(pp.get_prompt(datetime(*(TDAY + time))), expect)


    def testTagJustBefore(self):
        self.assertPromptEqual(
            expect='>>> ',
            time=(8, 59),
            json='["09:00", "15:00", "text"]',
            default_prompt='>>> ',
            tag_end_prompt='> '
            )

    def testTagStartTime(self):
        self.assertPromptEqual(
            expect='text> ',
            time=(9, 0),
            json='["09:00", "15:00", "text"]',
            default_prompt='>>> ',
            tag_end_prompt='> '
            )

    def testTagJustBeforeStop(self):
        self.assertPromptEqual(
            expect='text> ',
            time=(14, 59),
            json='["09:00", "15:00", "text"]',
            default_prompt='>>> ',
            tag_end_prompt='> '
            )

    def testTagStopTime(self):
        self.assertPromptEqual(
            expect='>>> ',
            time=(15, 0),
            json='["09:00", "15:00", "text"]',
            default_prompt='>>> ',
            tag_end_prompt='> '
            )

    def testTagEndAtMidnightJustBefore(self):
        self.assertPromptEqual(
            expect='text> ',
            time=(23, 59),
            json='["09:00", "00:00", "text"]',
            default_prompt='>>> ',
            tag_end_prompt='> '
            )

    def testTagEndAtMidnightAtMidnight(self):
        self.assertPromptEqual(
            expect='>>> ',
            time=(0, 0),
            json='["09:00", "00:00", "text"]',
            default_prompt='>>> ',
            tag_end_prompt='> '
            )

    def testTagStartAtMidnightJustBefore(self):
        self.assertPromptEqual(
            expect='>>> ',
            time=(23, 59),
            json='["00:00", "15:00", "text"]',
            default_prompt='>>> ',
            tag_end_prompt='> '
            )

    def testTagStartAtMidnightAtMidnight(self):
        self.assertPromptEqual(
            expect='text> ',
            time=(0, 0),
            json='["00:00", "15:00", "text"]',
            default_prompt='>>> ',
            tag_end_prompt='> '
            )

    def testTagOverlapPrecedingStartsFirst(self):
        self.assertPromptEqual(
            expect='str> ',
            time=(14, 30),
            json=('["09:00", "15:00", "text"], '
                  '["14:00", "15:00", "str"]'),
            default_prompt='>>> ',
            tag_end_prompt='> '
            )

    def testTagOverlapLatterStartsFirst(self):
        self.assertPromptEqual(
            expect='str> ',
            time=(14, 30),
            json=('["14:00", "15:00", "text"], '
                  '["09:00", "15:00", "str"]'),
            default_prompt='>>> ',
            tag_end_prompt='> '
            )

    def testTagOverlapMidJustBefore(self):
        self.assertPromptEqual(
            expect='text> ',
            time=(13, 59),
            json=('["09:00", "15:00", "text"], '
                  '["14:00", "15:00", "str"]'),
            default_prompt='>>> ',
            tag_end_prompt='> '
            )

    def testTagOverlapMidJustAfter(self):
        self.assertPromptEqual(
            expect='str> ',
            time=(14, 0),
            json=('["09:00", "15:00", "text"], '
                  '["14:00", "15:00", "str"]'),
            default_prompt='>>> ',
            tag_end_prompt='> '
            )

    def testTagOverlapEndJustBefore(self):
        self.assertPromptEqual(
            expect='str> ',
            time=(14, 59),
            json=('["09:00", "15:00", "text"], '
                  '["14:00", "16:00", "str"]'),
            default_prompt='>>> ',
            tag_end_prompt='> '
            )

    def testTagOverlapEndJustAfter(self):
        self.assertPromptEqual(
            expect='str> ',
            time=(15, 0),
            json=('["09:00", "15:00", "text"], '
                  '["14:00", "16:00", "str"]'),
            default_prompt='>>> ',
            tag_end_prompt='> '
            )

    def testTagOverlapBoundaryJustBefore(self):
        self.assertPromptEqual(
            expect='text> ',
            time=(10, 59),
            json=('["09:00", "11:00", "text"], '
                  '["11:00", "15:00", "str"]'),
            default_prompt='>>> ',
            tag_end_prompt='> '
            )

    def testTagOverlapBoundaryJustAfter(self):
        self.assertPromptEqual(
            expect='str> ',
            time=(11, 0),
            json=('["09:00", "11:00", "text"], '
                  '["11:00", "15:00", "str"]'),
            default_prompt='>>> ',
            tag_end_prompt='> '
            )


if __name__ == '__main__':
    unittest.main()
