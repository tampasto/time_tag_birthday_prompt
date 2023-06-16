from datetime import date
import unittest

from time_tag_birthday_prompt.primary_prompt import PrimaryPrompt
from time_tag_birthday_prompt.birthday_notifier import BirthdayNotifier

from time_tag_birthday_prompt.birthday import Birthday
from time_tag_birthday_prompt.exceptions import (
    IncorrectParameterTypeError, BirthdayNotifyDaysLessThanZeroError,
    LineWidthLessThanTenError
    )


class TestBirthdayNotifierInit(unittest.TestCase):
    """Test `BirthdayNotifier` object `__init__()` method."""


class TestBirthdayNotifierGetStr(unittest.TestCase):
    """Test `BirthdayNotifier` object `__str__()` method."""

    def testDaysFridayInWeek(self):
        birthday_notifier = BirthdayNotifier(birthday_notify_days=30, line_width=70)
        birthday_notifier.birthdays = [
            Birthday('2008-06-16', 'Abacus')
            ]
        msg_re = r'Birthday of Abacus \(15\) on Friday'
        gs = birthday_notifier.get_str(line_width=70, today=date(2023, 6, 10))
        self.assertRegex(gs, msg_re.replace(' ', r'\s+'))

    def testDaysSaturdayNextWeek(self):
        birthday_notifier = BirthdayNotifier(birthday_notify_days=30, line_width=70)
        birthday_notifier.birthdays = [
            Birthday('2008-06-17', 'Abacus')
            ]
        msg_re = r'Birthday of Abacus \(15\) on Saturday next week'
        gs = birthday_notifier.get_str(line_width=70, today=date(2023, 6, 10))
        self.assertRegex(gs, msg_re.replace(' ', r'\s+'))

    def testDaysSundayNextWeek(self):
        birthday_notifier = BirthdayNotifier(birthday_notify_days=30, line_width=70)
        birthday_notifier.birthdays = [
            Birthday('2008-06-18', 'Abacus')
            ]
        msg_re = r'Birthday of Abacus \(15\) on Sunday next week'
        gs = birthday_notifier.get_str(line_width=70, today=date(2023, 6, 5))
        self.assertRegex(gs, msg_re.replace(' ', r'\s+'))

    def testDaysIn14Days(self):
        birthday_notifier = BirthdayNotifier(birthday_notify_days=30, line_width=70)
        birthday_notifier.birthdays = [
            Birthday('2008-06-18', 'Abacus')
            ]
        msg_re = r'Birthday of Abacus \(15\) in 14 days'
        gs = birthday_notifier.get_str(line_width=70, today=date(2023, 6, 4))
        self.assertRegex(gs, msg_re.replace(' ', r'\s+'))

    def testDaysNoLeapDay(self):
        birthday_notifier = BirthdayNotifier(birthday_notify_days=30, line_width=70)
        birthday_notifier.birthdays = [
            Birthday('2008-03-01', 'Abacus')
            ]
        msg_re = r'Birthday of Abacus \(15\) in 10 days'
        gs = birthday_notifier.get_str(line_width=70, today=date(2023, 2, 19))
        self.assertRegex(gs, msg_re.replace(' ', r'\s+'))

    def testDaysLeapDay(self):
        birthday_notifier = BirthdayNotifier(birthday_notify_days=30, line_width=70)
        birthday_notifier.birthdays = [
            Birthday('2008-03-01', 'Abacus')
            ]
        msg_re = r'Birthday of Abacus \(16\) in 12 days'
        gs = birthday_notifier.get_str(line_width=70, today=date(2024, 2, 18))
        self.assertRegex(gs, msg_re.replace(' ', r'\s+'))

    def testDaysTomorrow(self):
        birthday_notifier = BirthdayNotifier(birthday_notify_days=30, line_width=70)
        birthday_notifier.birthdays = [
            Birthday('2008-08-02', 'Abacus')
            ]
        msg_re = r'Birthday of Abacus \(15\) tomorrow'
        gs = birthday_notifier.get_str(line_width=70, today=date(2023, 8, 1))
        self.assertRegex(gs, msg_re.replace(' ', r'\s+'))

    def testDaysToday(self):
        birthday_notifier = BirthdayNotifier(birthday_notify_days=30, line_width=70)
        birthday_notifier.birthdays = [
            Birthday('2008-08-01', 'Abacus')
            ]
        msg_re = r'Birthday of Abacus \(15\) today'
        gs = birthday_notifier.get_str(line_width=70, today=date(2023, 8, 1))
        self.assertRegex(gs, msg_re.replace(' ', r'\s+'))

    def testTwoPeopleDifferentDays(self):
        birthday_notifier = BirthdayNotifier(birthday_notify_days=30, line_width=70)
        birthday_notifier.birthdays = [
            Birthday('2008-08-01', 'Abacus'),
            Birthday('2007-07-31', 'Bacillus')
            ]
        msg_re = r'Birthday of Bacillus \(16\) in 8 days, Abacus \(15\) in 9 days'
        gs = birthday_notifier.get_str(line_width=70, today=date(2023, 7, 23))
        self.assertRegex(gs, msg_re.replace(' ', r'\s+'))

    def testThreePeopleDifferentDays(self):
        birthday_notifier = BirthdayNotifier(birthday_notify_days=30, line_width=70)
        birthday_notifier.birthdays = [
            Birthday('2008-08-02', 'Abacus'),
            Birthday('2007-08-01', 'Bacillus'),
            Birthday('2006-07-31', 'Cecil')
            ]
        msg_re = r'Birthday of Cecil \(17\) in 8 days, Bacillus \(16\) in 9 days, Abacus \(15\) in 10 days'
        gs = birthday_notifier.get_str(line_width=70, today=date(2023, 7, 23))
        self.assertRegex(gs, msg_re.replace(' ', r'\s+'))

    def testTwoPeopleSameDayAlphaAscending(self):
        birthday_notifier = BirthdayNotifier(birthday_notify_days=30, line_width=70)
        birthday_notifier.birthdays = [
            Birthday('2007-08-01', 'Bacillus'),
            Birthday('2008-08-01', 'Abacus')
            ]
        msg_re = r'Birthday of Abacus \(15\) and Bacillus \(16\) in 9 days'
        gs = birthday_notifier.get_str(line_width=70, today=date(2023, 7, 23))
        self.assertRegex(gs, msg_re.replace(' ', r'\s+'))

    def testThreePeopleSameDayAlphaAscending(self):
        birthday_notifier = BirthdayNotifier(birthday_notify_days=30, line_width=70)
        birthday_notifier.birthdays = [
            Birthday('2006-08-01', 'Cecil'),
            Birthday('2008-08-01', 'Abacus'),
            Birthday('2007-08-01', 'Bacillus')
            ]
        msg_re = r'Birthday of Abacus \(15\), Bacillus \(16\) and Cecil \(17\) on Tuesday'
        gs = birthday_notifier.get_str(line_width=70, today=date(2023, 7, 26))
        self.assertRegex(gs, msg_re.replace(' ', r'\s+'))


if __name__ == '__main__':
    unittest.main()
