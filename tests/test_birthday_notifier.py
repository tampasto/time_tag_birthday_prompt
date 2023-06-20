from datetime import date
from tempfile import TemporaryFile
import unittest

from .extend_unittest import OverridePrint
from time_tag_birthday_prompt.birthday_notifier import BirthdayNotifier

from time_tag_birthday_prompt.primary_prompt import PrimaryPrompt
from time_tag_birthday_prompt.data_loader import DataLoader
from time_tag_birthday_prompt.exceptions import (
    IncorrectParameterTypeError
    )


def get_birthday_notifier(
        birthday_array_text, birthday_notify_days=30) -> BirthdayNotifier:
    bn = None
    with TemporaryFile(mode='w+', encoding='utf-8') as tf:
        tf.write(
            '{"timeTags": null, "birthdays": [' + birthday_array_text + ']}'
            )
        tf.seek(0)
        bn = BirthdayNotifier(
            data_loader=DataLoader(file_obj=tf, path='<testing>'),
            birthday_notify_days=birthday_notify_days,
            line_width=70
            )
    return bn


class TestBirthdayNotifier__init__(unittest.TestCase):
    """Test `BirthdayNotifier` object `__init__()` method."""

    def testParam_data_loader_isGiven(self):
        bn = get_birthday_notifier(
                '["1950-01-01", "name"], ["1951-02-02", "name2"]')
        match_count = 0
        for bday in bn.birthdays:
            if (bday.name == 'name' and bday.date_obj.year == 1950
                and bday.date_obj.month == 1 and bday.date_obj.day == 1):
                match_count += 1
            elif (bday.name == 'name2' and bday.date_obj.year == 1951
                and bday.date_obj.month == 2 and bday.date_obj.day == 2):
                match_count += 1
        self.assertEqual(match_count, 2)

    def testParam_data_loader_isNotGiven(self):
        bn = BirthdayNotifier(
            data_loader=None,
            birthday_notify_days=30,
            line_width=70
            )
        self.assertIsNone(bn.birthdays)

    def testParam_birthday_notify_days_isRedirected(self):
        pp = PrimaryPrompt(birthday_notify_days=90)
        self.assertEqual(pp.birthday_notifier.birthday_notify_days, 90)

    def testParam_line_width_isRedirected(self):
        pp = PrimaryPrompt(line_width=100)
        self.assertEqual(pp.birthday_notifier.line_width, 100)


class TestBirthdayNotifier_time_machine(unittest.TestCase):
    """Test `BirthdayNotifier` object `time_machine()` method."""

    def testParam_date_string_incorrectType(self):
        bn = BirthdayNotifier(
            data_loader=None,
            birthday_notify_days=30,
            line_width=70
            )
        op = OverridePrint()
        with self.assertRaises(IncorrectParameterTypeError):
            bn.time_machine(
                date_string=date(2023, 6, 10), print_func=op)

    def testParam_print_func_incorrectType(self):
        bn = BirthdayNotifier(
            data_loader=None,
            birthday_notify_days=30,
            line_width=70
            )
        with self.assertRaises(IncorrectParameterTypeError):
            bn.time_machine(
                date_string='2023-06-10', print_func='OverridePrint')

    def testIfWorks(self):
        bn = get_birthday_notifier(
                '["2008-06-16", "Abacus"]',
                birthday_notify_days=30
                )
        op = OverridePrint()
        bn.time_machine(date_string='2023-06-10', print_func=op)
        op.text = ' '.join(op.text.split())
        self.assertIn('Birthday of Abacus (15) on Friday -', op.text)


class TestBirthdayNotifier_print_birthdays(unittest.TestCase):
    """Test `BirthdayNotifier` object `print_birthdays()` method."""

    def testIfWorks(self):
        bn = get_birthday_notifier(
                '["2008-06-16", "Abacus"], '
                '["2007-06-17", "Bacillus"], '
                '["2006-06-18", "Cecil"]',
                birthday_notify_days=30
                )
        req_matches = (
            '2008-06-16 Abacus',
            '2007-06-17 Bacillus',
            '2006-06-18 Cecil'
        )

        op = OverridePrint()
        bn.print_birthdays(print_func=op)
        match_count = 0
        for line in op.text.split('\n'):
            if ' '.join(line.split()) in req_matches:
                match_count += 1
        self.assertEqual(match_count, 3)



class TestBirthdayNotifier_get_str(unittest.TestCase):
    """Test `BirthdayNotifier` object `get_str()` method."""

    def testDaysFridayInWeek(self):
        bn = get_birthday_notifier(
                '["2008-06-16", "Abacus"]',
                birthday_notify_days=30
                )
        gs = bn.get_str(today=date(2023, 6, 10))
        gs = ' '.join(gs.split())
        self.assertIn('Birthday of Abacus (15) on Friday -', gs)

    def testDaysSaturdayNextWeek(self):
        bn = get_birthday_notifier(
                '["2008-06-17", "Abacus"]',
                birthday_notify_days=30
                )
        gs = bn.get_str(today=date(2023, 6, 10))
        gs = ' '.join(gs.split())
        self.assertIn('Birthday of Abacus (15) on Saturday next week -', gs)

    def testDaysSundayNextWeek(self):
        bn = get_birthday_notifier(
                '["2008-06-18", "Abacus"]',
                birthday_notify_days=30
                )
        gs = bn.get_str(today=date(2023, 6, 5))
        gs = ' '.join(gs.split())
        self.assertIn('Birthday of Abacus (15) on Sunday next week -', gs)

    def testDaysIn14Days(self):
        bn = get_birthday_notifier(
                '["2008-06-18", "Abacus"]',
                birthday_notify_days=30
                )
        gs = bn.get_str(today=date(2023, 6, 4))
        gs = ' '.join(gs.split())
        self.assertIn('Birthday of Abacus (15) in 14 days -', gs)

    def testDaysNoLeapDay(self):
        bn = get_birthday_notifier(
                '["2008-03-01", "Abacus"]',
                birthday_notify_days=30
                )
        gs = bn.get_str(today=date(2023, 2, 19))
        gs = ' '.join(gs.split())
        self.assertIn('Birthday of Abacus (15) in 10 days -', gs)

    def testDaysLeapDay(self):
        bn = get_birthday_notifier(
                '["2008-03-01", "Abacus"]',
                birthday_notify_days=30
                )
        gs = bn.get_str(today=date(2024, 2, 18))
        gs = ' '.join(gs.split())
        self.assertIn('Birthday of Abacus (16) in 12 days -', gs)

    def testDaysTomorrow(self):
        bn = get_birthday_notifier(
                '["2008-08-02", "Abacus"]',
                birthday_notify_days=30
                )
        gs = bn.get_str(today=date(2023, 8, 1))
        gs = ' '.join(gs.split())
        self.assertIn('Birthday of Abacus (15) tomorrow -', gs)

    def testDaysToday(self):
        bn = get_birthday_notifier(
                '["2008-08-01", "Abacus"]',
                birthday_notify_days=30
                )
        gs = bn.get_str(today=date(2023, 8, 1))
        gs = ' '.join(gs.split())
        self.assertIn('Birthday of Abacus (15) today -', gs)

    def testTwoPeopleDifferentDays(self):
        bn = get_birthday_notifier(
                '["2008-08-01", "Abacus"], '
                '["2007-07-31", "Bacillus"]',
                birthday_notify_days=30
                )
        gs = bn.get_str(today=date(2023, 7, 23))
        gs = ' '.join(gs.split())
        self.assertIn('Birthday of Bacillus (16) in 8 days, Abacus (15) in 9 days -', gs)

    def testThreePeopleDifferentDays(self):
        bn = get_birthday_notifier(
                '["2008-08-02", "Abacus"], '
                '["2007-08-01", "Bacillus"], '
                '["2006-07-31", "Cecil"]',
                birthday_notify_days=30
                )
        gs = bn.get_str(today=date(2023, 7, 23))
        gs = ' '.join(gs.split())
        self.assertIn('Birthday of Cecil (17) in 8 days, Bacillus (16) in 9 days, Abacus (15) in 10 days -', gs)

    def testTwoPeopleSameDayAlphaAscending(self):
        bn = get_birthday_notifier(
                '["2007-08-01", "Bacillus"], '
                '["2008-08-01", "Abacus"]',
                birthday_notify_days=30
                )
        gs = bn.get_str(today=date(2023, 7, 23))
        gs = ' '.join(gs.split())
        self.assertIn('Birthday of Abacus (15) and Bacillus (16) in 9 days -', gs)

    def testThreePeopleSameDayAlphaAscending(self):
        bn = get_birthday_notifier(
                '["2006-08-01", "Cecil"], '
                '["2008-08-01", "Abacus"], '
                '["2007-08-01", "Bacillus"]',
                birthday_notify_days=30
                )
        gs = bn.get_str(today=date(2023, 7, 26))
        gs = ' '.join(gs.split())
        self.assertIn('Birthday of Abacus (15), Bacillus (16) and Cecil (17) on Tuesday -', gs)

    def testNotifyDays30TwoPeopleNoneWithin(self):
        bn = get_birthday_notifier(
                '["2008-08-01", "Abacus"], '
                '["2007-07-31", "Bacillus"]',
                birthday_notify_days=30
                )
        gs = bn.get_str(today=date(2023, 6, 30))
        gs = ' '.join(gs.split())
        self.assertIn(', 2023-06-30 -', gs)

    def testNotifyDays30TwoPeopleOneWithin(self):
        bn = get_birthday_notifier(
                '["2008-08-01", "Abacus"], '
                '["2007-07-31", "Bacillus"]',
                birthday_notify_days=30
                )
        gs = bn.get_str(today=date(2023, 7, 1))
        gs = ' '.join(gs.split())
        self.assertIn('Birthday of Bacillus (16) in 30 days -', gs)

    def testNotifyDays30TwoPeopleBothWithin(self):
        bn = get_birthday_notifier(
                '["2008-08-01", "Abacus"], '
                '["2007-07-31", "Bacillus"]',
                birthday_notify_days=30
                )
        gs = bn.get_str(today=date(2023, 7, 2))
        gs = ' '.join(gs.split())
        self.assertIn('Birthday of Bacillus (16) in 29 days, Abacus (15) in 30 days -', gs)

    def testNoYearDaysFridayInWeek(self):
        bn = get_birthday_notifier(
                '["06-16", "Abacus"]',
                birthday_notify_days=30
                )
        gs = bn.get_str(today=date(2023, 6, 10))
        gs = ' '.join(gs.split())
        self.assertIn('Birthday of Abacus on Friday -', gs)

    def testNoYearDaysIn14Days(self):
        bn = get_birthday_notifier(
                '["06-18", "Abacus"]',
                birthday_notify_days=30
                )
        gs = bn.get_str(today=date(2023, 6, 4))
        gs = ' '.join(gs.split())
        self.assertIn('Birthday of Abacus in 14 days -', gs)

    def testNotifyDays1DayAfterTomorrow(self):
        bn = get_birthday_notifier(
                '["2008-07-01", "Abacus"]',
                birthday_notify_days=1
                )
        gs = bn.get_str(today=date(2023, 6, 29))
        gs = ' '.join(gs.split())
        self.assertIn(', 2023-06-29 -', gs)

    def testNotifyDays1Tomorrow(self):
        bn = get_birthday_notifier(
                '["2008-07-01", "Abacus"]',
                birthday_notify_days=1
                )
        gs = bn.get_str(today=date(2023, 6, 30))
        gs = ' '.join(gs.split())
        self.assertIn('Birthday of Abacus (15) tomorrow -', gs)

    def testNotifyDays1Today(self):
        bn = get_birthday_notifier(
                '["2008-07-01", "Abacus"]',
                birthday_notify_days=1
                )
        gs = bn.get_str(today=date(2023, 7, 1))
        gs = ' '.join(gs.split())
        self.assertIn('Birthday of Abacus (15) today -', gs)

    def testNotifyDays0Tomorrow(self):
        bn = get_birthday_notifier(
                '["2008-07-01", "Abacus"]',
                birthday_notify_days=0
                )
        gs = bn.get_str(today=date(2023, 6, 30))
        gs = ' '.join(gs.split())
        self.assertIn(', 2023-06-30 -', gs)

    def testNotifyDays0Today(self):
        bn = get_birthday_notifier(
                '["2008-07-01", "Abacus"]',
                birthday_notify_days=0
                )
        gs = bn.get_str(today=date(2023, 7, 1))
        gs = ' '.join(gs.split())
        self.assertIn('Birthday of Abacus (15) today -', gs)


if __name__ == '__main__':
    unittest.main()
