from datetime import datetime
from tempfile import TemporaryFile
from typing import Tuple
import unittest

from time_tag_birthday_prompt.secondary_prompt import SecondaryPrompt

from time_tag_birthday_prompt.data_loader import DataLoader
from time_tag_birthday_prompt.exceptions import IncorrectParameterTypeError
from time_tag_birthday_prompt.primary_prompt import PrimaryPrompt

TDAY = 2023, 6, 10


class TestSecondaryPrompt__init__(unittest.TestCase):

    def testParam_primary_prompt_incorrectType(self):
        with self.assertRaises(IncorrectParameterTypeError):
            SecondaryPrompt(primary_prompt=None)

    def testParam_prompt_incorrectType(self):
        with self.assertRaises(IncorrectParameterTypeError):
            SecondaryPrompt(primary_prompt=PrimaryPrompt(), prompt=42)


class TestSecondaryPrompt_get_str(unittest.TestCase):
    """Test `PrimaryPrompt` object `get_str()` method."""

    def assertPromptEqual(
            self, expect: str, time: Tuple[int, int], json: str,
            prompt='... ', default_prompt: str = '>>> ', 
            tag_end_prompt: str = '> '):
        dl = None
        with TemporaryFile(mode='w+', encoding='utf-8') as tf:
            tf.write(
                '{"timeTags": [' + json + '], '
                '"birthdays": null}'
                )
            tf.seek(0)
            dl = DataLoader(tf, '<testing>')
        pp = PrimaryPrompt(
            default_prompt=default_prompt,
            tag_end_prompt=tag_end_prompt,
            data_loader=dl
            )
        sp = SecondaryPrompt(primary_prompt=pp, prompt=prompt)
        self.assertEqual(sp.get_str(datetime(*(TDAY + time))), expect)

    def testActiveTag4End2Long(self):
        self.assertPromptEqual(
            expect='  ... ',
            time=(12, 0),
            json='["09:00", "15:00", "text"]',
            prompt='... ',
            default_prompt='>>> ',
            tag_end_prompt='> '
            )

    def testActiveTag6End2Long(self):
        self.assertPromptEqual(
            expect='    ... ',
            time=(12, 0),
            json='["09:00", "15:00", "textAB"]',
            prompt='... ',
            default_prompt='>>> ',
            tag_end_prompt='> '
            )

    def testActiveTag1End2Long(self):
        self.assertPromptEqual(
            expect='... ',
            time=(12, 0),
            json='["09:00", "15:00", "t"]',
            prompt='... ',
            default_prompt='>>> ',
            tag_end_prompt='> '
            )

    def testActiveTag1End5Long(self):
        self.assertPromptEqual(
            expect='  ... ',
            time=(12, 0),
            json='["09:00", "15:00", "t"]',
            prompt='... ',
            default_prompt='>>> ',
            tag_end_prompt='>>>> '
            )

    def testActiveTag0End2Long(self):
        self.assertPromptEqual(
            expect='... ',
            time=(12, 0),
            json='["09:00", "15:00", ""]',
            prompt='... ',
            default_prompt='>>> ',
            tag_end_prompt='> '
            )

    def testActiveTag4End2Secondary2Long(self):
        self.assertPromptEqual(
            expect='    . ',
            time=(12, 0),
            json='["09:00", "15:00", "text"]',
            prompt='. ',
            default_prompt='>>> ',
            tag_end_prompt='> '
            )

    def testActiveTag4End2Secondary6Long(self):
        self.assertPromptEqual(
            expect='..... ',
            time=(12, 0),
            json='["09:00", "15:00", "text"]',
            prompt='..... ',
            default_prompt='>>> ',
            tag_end_prompt='> '
            )

    def testActiveTag4End1Secondary6Long(self):
        self.assertPromptEqual(
            expect='..... ',
            time=(12, 0),
            json='["09:00", "15:00", "text"]',
            prompt='..... ',
            default_prompt='>>> ',
            tag_end_prompt='> '
            )

    def testInactiveDefault(self):
        self.assertPromptEqual(
            expect='... ',
            time=(8, 0),
            json='["09:00", "15:00", "text"]',
            prompt='... ',
            default_prompt='>>> ',
            tag_end_prompt='> '
            )

    def testInactivePrimary6Secondary4Long(self):
        self.assertPromptEqual(
            expect='  ... ',
            time=(8, 0),
            json='["09:00", "15:00", "text"]',
            prompt='... ',
            default_prompt='>>>>> ',
            tag_end_prompt='> '
            )

    def testInactivePrimary2Secondary4Long(self):
        self.assertPromptEqual(
            expect='... ',
            time=(8, 0),
            json='["09:00", "15:00", "text"]',
            prompt='... ',
            default_prompt='> ',
            tag_end_prompt='> '
            )

    def testInactivePrimary4Secondary6Long(self):
        self.assertPromptEqual(
            expect='..... ',
            time=(8, 0),
            json='["09:00", "15:00", "text"]',
            prompt='..... ',
            default_prompt='>>> ',
            tag_end_prompt='> '
            )

    def testInactivePrimary4Secondary2Long(self):
        self.assertPromptEqual(
            expect='  . ',
            time=(8, 0),
            json='["09:00", "15:00", "text"]',
            prompt='. ',
            default_prompt='>>> ',
            tag_end_prompt='> '
            )


if __name__ == '__main__':
    unittest.main()
