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

    def call_get_str(
            self, json: str, return_second_call: bool,
            second_call_date_obj: datetime | None = None
            ) -> str:
        dl = None
        with TemporaryFile(mode='w+', encoding='utf-8') as tf:
            tf.write(json)
            tf.seek(0)
            dl = DataLoader(tf, '<testing>')
        pp = PrimaryPrompt(
            birthday_notify_days=30,
            line_width = 70,
            data_loader=dl
            )
        date_obj = datetime(2023, 6, 15, 12, 30, 15)
        if return_second_call:
            pp.get_str(date_obj)
            if second_call_date_obj:
                date_obj = second_call_date_obj
            return pp.get_str(date_obj)
        else:
            return pp.get_str(date_obj)

    def testPrologMessagesTimeTagFormatError(self):
        gs = self.call_get_str(
            '{"timeTags": [["xx:00", "15:00", "text"]], "birthdays": null}',
            return_second_call=False
            )
        gs = ' '.join(gs.split())
        self.assertIn("Incorrect start time format 'xx:00' for tag 'text'. Expected HH:MM.", gs)

    def testPrologMessagesBirthdayFormatError(self):
        gs = self.call_get_str(
            '{"timeTags": null, "birthdays": [["xxxx-01-01", "name"]]}',
            return_second_call=False
            )
        gs = ' '.join(gs.split())
        self.assertIn("Incorrect birthday format 'xxxx-01-01' for 'name'. Expected YYYY-MM-DD or MM-DD.", gs)

    def testPrologMessagesTimeTagAndBirthdayFormatError(self):
        gs = self.call_get_str(
            '{"timeTags": [["xx:00", "15:00", "text"]], '
            '"birthdays": [["xxxx-01-01", "name"]]}',
            return_second_call=False
            )
        gs = ' '.join(gs.split())
        self.assertTrue(
            "Incorrect start time format 'xx:00' for tag 'text'. Expected HH:MM." in gs
            and "Incorrect birthday format 'xxxx-01-01' for 'name'. Expected YYYY-MM-DD or MM-DD." in gs
            )

    def testPrologMessagesTimeTagFormatErrorSecondCall(self):
        gs = self.call_get_str(
            '{"timeTags": [["xx:00", "15:00", "text"]], "birthdays": null}',
            return_second_call=True
            )
        gs = ' '.join(gs.split())
        self.assertNotIn("Incorrect start time format 'xx:00' for tag 'text'. Expected HH:MM.", gs)

    def testPrologMessagesBirthdayFormatErrorSecondCall(self):
        gs = self.call_get_str(
            '{"timeTags": null, "birthdays": [["xxxx-01-01", "name"]]}',
            return_second_call=True
            )
        gs = ' '.join(gs.split())
        self.assertNotIn("Incorrect birthday format 'xxxx-01-01' for 'name'. Expected YYYY-MM-DD or MM-DD.", gs)

    def testPrologMessagesTimeTagAndBirthdayFormatErrorSecondCall(self):
        gs = self.call_get_str(
            '{"timeTags": [["xx:00", "15:00", "text"]], '
            '"birthdays": [["xxxx-01-01", "name"]]}',
            return_second_call=True
            )
        gs = ' '.join(gs.split())
        self.assertTrue(
            "Incorrect start time format 'xx:00' for tag 'text'. Expected HH:MM." not in gs
            and "Incorrect birthday format 'xxxx-01-01' for 'name'. Expected YYYY-MM-DD or MM-DD." not in gs
            )

    def testPrologMessagesBirthdayFirstCall(self):
        gs = self.call_get_str(
            '{"timeTags": null, "birthdays": [["1950-06-16", "name"]]}',
            return_second_call=False
            )
        gs = ' '.join(gs.split())
        # datetime: 2023-06-15 12:30:15
        self.assertIn('Birthday of name (73) tomorrow', gs)

    def testPrologMessagesBirthdaySecondCallBeforeMidnight(self):
        gs = self.call_get_str(
            '{"timeTags": null, "birthdays": [["1950-06-16", "name"]]}',
            return_second_call=True,
            second_call_date_obj=datetime(2023, 6, 15, 23, 59, 59)
            )
        gs = ' '.join(gs.split())
        # datetime first call: 2023-06-15 12:30:15
        self.assertNotIn('Birthday of name (73) tomorrow', gs)

    def testPrologMessagesBirthdaySecondCallAfterMidnight(self):
        gs = self.call_get_str(
            '{"timeTags": null, "birthdays": [["1950-06-16", "name"]]}',
            return_second_call=True,
            second_call_date_obj=datetime(2023, 6, 16, 0, 0, 0)
            )
        gs = ' '.join(gs.split())
        # datetime first call: 2023-06-15 12:30:15
        self.assertIn('Birthday of name (73) today', gs)

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
