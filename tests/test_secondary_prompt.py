from datetime import datetime
import unittest

from time_tag_birthday_prompt.secondary_prompt import SecondaryPrompt

from time_tag_birthday_prompt.exceptions import IncorrectParameterTypeError
from time_tag_birthday_prompt.primary_prompt import PrimaryPrompt
from time_tag_birthday_prompt.time_tag import TimeTag

TDAY = 2023, 6, 10


class TestSecondaryPromptInit(unittest.TestCase):

    def testIncorrectParameterTypeError(self):
        with self.assertRaises(IncorrectParameterTypeError):
            SecondaryPrompt(primary_prompt=None)

    def testIncorrectParameterTypeError(self):
        with self.assertRaises(IncorrectParameterTypeError):
            SecondaryPrompt(primary_prompt=PrimaryPrompt(), prompt=42)


class TestSecondaryPromptGetStr(unittest.TestCase):
    """Test `PrimaryPrompt` object `__str__()` method."""

    def testActiveTag4End2Long(self):
        primary_prompt = PrimaryPrompt(default_prompt='>>> ', tag_end_prompt='> ')
        primary_prompt.time_tags = [
            TimeTag('09:00', '15:00', 'text')
        ]
        secondary_prompt = SecondaryPrompt(primary_prompt=primary_prompt, prompt='... ')
        self.assertEqual(secondary_prompt.get_str(datetime(*TDAY, 12, 0)), '  ... ')

    def testActiveTag6End2Long(self):
        primary_prompt = PrimaryPrompt(default_prompt='>>> ', tag_end_prompt='> ')
        primary_prompt.time_tags = [
            TimeTag('09:00', '15:00', 'textAB')
        ]
        secondary_prompt = SecondaryPrompt(primary_prompt=primary_prompt, prompt='... ')
        self.assertEqual(secondary_prompt.get_str(datetime(*TDAY, 12, 0)), '    ... ')

    def testActiveTag1End2Long(self):
        primary_prompt = PrimaryPrompt(default_prompt='>>> ', tag_end_prompt='> ')
        primary_prompt.time_tags = [
            TimeTag('09:00', '15:00', 't')
        ]
        secondary_prompt = SecondaryPrompt(primary_prompt=primary_prompt, prompt='... ')
        self.assertEqual(secondary_prompt.get_str(datetime(*TDAY, 12, 0)), '... ')

    def testActiveTag1End5Long(self):
        primary_prompt = PrimaryPrompt(default_prompt='>>> ', tag_end_prompt='>>>> ')
        primary_prompt.time_tags = [
            TimeTag('09:00', '15:00', 't')
        ]
        secondary_prompt = SecondaryPrompt(primary_prompt=primary_prompt, prompt='... ')
        self.assertEqual(secondary_prompt.get_str(datetime(*TDAY, 12, 0)), '  ... ')

    def testActiveTag0End2Long(self):
        primary_prompt = PrimaryPrompt(default_prompt='>>> ', tag_end_prompt='> ')
        primary_prompt.time_tags = [
            TimeTag('09:00', '15:00', '')
        ]
        secondary_prompt = SecondaryPrompt(primary_prompt=primary_prompt, prompt='... ')
        self.assertEqual(secondary_prompt.get_str(datetime(*TDAY, 12, 0)), '... ')

    def testActiveTag4End2Secondary2Long(self):
        primary_prompt = PrimaryPrompt(default_prompt='>>> ', tag_end_prompt='> ')
        primary_prompt.time_tags = [
            TimeTag('09:00', '15:00', 'text')
        ]
        secondary_prompt = SecondaryPrompt(primary_prompt=primary_prompt, prompt='. ')
        self.assertEqual(secondary_prompt.get_str(datetime(*TDAY, 12, 0)), '    . ')

    def testActiveTag4End2Secondary6Long(self):
        primary_prompt = PrimaryPrompt(default_prompt='>>> ', tag_end_prompt='> ')
        primary_prompt.time_tags = [
            TimeTag('09:00', '15:00', 'text')
        ]
        secondary_prompt = SecondaryPrompt(primary_prompt=primary_prompt, prompt='..... ')
        self.assertEqual(secondary_prompt.get_str(datetime(*TDAY, 12, 0)), '..... ')

    def testActiveTag4End1Secondary6Long(self):
        primary_prompt = PrimaryPrompt(default_prompt='>>> ', tag_end_prompt='>')
        primary_prompt.time_tags = [
            TimeTag('09:00', '15:00', 'text')
        ]
        secondary_prompt = SecondaryPrompt(primary_prompt=primary_prompt, prompt='..... ')
        self.assertEqual(secondary_prompt.get_str(datetime(*TDAY, 12, 0)), '..... ')

    def testInactiveDefault(self):
        primary_prompt = PrimaryPrompt(default_prompt='>>> ', tag_end_prompt='> ')
        primary_prompt.time_tags = [
            TimeTag('09:00', '15:00', 'text')
        ]
        secondary_prompt = SecondaryPrompt(primary_prompt=primary_prompt, prompt='... ')
        self.assertEqual(secondary_prompt.get_str(datetime(*TDAY, 8, 0)), '... ')

    def testInactivePrimary6Secondary4Long(self):
        primary_prompt = PrimaryPrompt(default_prompt='>>>>> ', tag_end_prompt='> ')
        primary_prompt.time_tags = [
            TimeTag('09:00', '15:00', 'text')
        ]
        secondary_prompt = SecondaryPrompt(primary_prompt=primary_prompt, prompt='... ')
        self.assertEqual(secondary_prompt.get_str(datetime(*TDAY, 8, 0)), '  ... ')

    def testInactivePrimary2Secondary4Long(self):
        primary_prompt = PrimaryPrompt(default_prompt='> ', tag_end_prompt='> ')
        primary_prompt.time_tags = [
            TimeTag('09:00', '15:00', 'text')
        ]
        secondary_prompt = SecondaryPrompt(primary_prompt=primary_prompt, prompt='... ')
        self.assertEqual(secondary_prompt.get_str(datetime(*TDAY, 8, 0)), '... ')

    def testInactivePrimary4Secondary6Long(self):
        primary_prompt = PrimaryPrompt(default_prompt='>>> ', tag_end_prompt='> ')
        primary_prompt.time_tags = [
            TimeTag('09:00', '15:00', 'text')
        ]
        secondary_prompt = SecondaryPrompt(primary_prompt=primary_prompt, prompt='..... ')
        self.assertEqual(secondary_prompt.get_str(datetime(*TDAY, 8, 0)), '..... ')

    def testInactivePrimary4Secondary2Long(self):
        primary_prompt = PrimaryPrompt(default_prompt='>>> ', tag_end_prompt='> ')
        primary_prompt.time_tags = [
            TimeTag('09:00', '15:00', 'text')
        ]
        secondary_prompt = SecondaryPrompt(primary_prompt=primary_prompt, prompt='. ')
        self.assertEqual(secondary_prompt.get_str(datetime(*TDAY, 8, 0)), '  . ')


if __name__ == '__main__':
    unittest.main()
