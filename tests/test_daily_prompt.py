from datetime import date
import unittest

from time_tag_birthday_prompt.daily_prompt import DailyPrompt

from time_tag_birthday_prompt.birthday import Birthday


class TestDailyPromptInit(unittest.TestCase):
    """Test `DailyPrompt` object `__init__()` method."""

    def testDaysWrongType(self):
        daily_prompt = DailyPrompt(birthday_notify_days=(5, 6))
        msg_re = r"Parameter 'birthday_notify_days' is not of type int."
        self.assertRegex(str(daily_prompt), msg_re.replace(' ', r'\s+'))
    
    def testDaysOutOfRangeMinusOne(self):
        daily_prompt = DailyPrompt(birthday_notify_days=-1)
        msg_re = r'Parameter birthday_notify_days=[0-9\-]+ is out of range.'
        self.assertRegex(str(daily_prompt), msg_re.replace(' ', r'\s+'))

    def testLineWidthWrongType(self):
        daily_prompt = DailyPrompt(line_width=(5, 6))
        msg_re = r"Parameter 'line_width' is not of type int."
        self.assertRegex(str(daily_prompt), msg_re.replace(' ', r'\s+'))
    
    def testLineWidthOutOfRangeZero(self):
        daily_prompt = DailyPrompt(line_width=0)
        msg_re = r'Parameter line_width=[0-9\-]+ is out of range.'
        self.assertRegex(str(daily_prompt), msg_re.replace(' ', r'\s+'))


class TestDailyPromptGetStr(unittest.TestCase):
    """Test `DailyPrompt` object `__str__()` method."""

    def testDaysFridayInWeek(self):
        daily_prompt = DailyPrompt(birthday_notify_days=30, line_width=70)
        daily_prompt.birthdays = [
            Birthday('2008-06-16', 'Abacus')
            ]
        msg_re = r'Birthday of Abacus \(15\) on Friday'
        gs = daily_prompt.get_str(line_width=70, today=date(2023, 6, 10))
        self.assertRegex(gs, msg_re.replace(' ', r'\s+'))

    def testDaysSaturdayNextWeek(self):
        daily_prompt = DailyPrompt(birthday_notify_days=30, line_width=70)
        daily_prompt.birthdays = [
            Birthday('2008-06-17', 'Abacus')
            ]
        msg_re = r'Birthday of Abacus \(15\) on Saturday next week'
        gs = daily_prompt.get_str(line_width=70, today=date(2023, 6, 10))
        self.assertRegex(gs, msg_re.replace(' ', r'\s+'))

    def testDaysSundayNextWeek(self):
        daily_prompt = DailyPrompt(birthday_notify_days=30, line_width=70)
        daily_prompt.birthdays = [
            Birthday('2008-06-18', 'Abacus')
            ]
        msg_re = r'Birthday of Abacus \(15\) on Sunday next week'
        gs = daily_prompt.get_str(line_width=70, today=date(2023, 6, 5))
        self.assertRegex(gs, msg_re.replace(' ', r'\s+'))

    def testDaysIn14Days(self):
        daily_prompt = DailyPrompt(birthday_notify_days=30, line_width=70)
        daily_prompt.birthdays = [
            Birthday('2008-06-18', 'Abacus')
            ]
        msg_re = r'Birthday of Abacus \(15\) in 14 days'
        gs = daily_prompt.get_str(line_width=70, today=date(2023, 6, 4))
        self.assertRegex(gs, msg_re.replace(' ', r'\s+'))

    def testDaysNoLeapDay(self):
        daily_prompt = DailyPrompt(birthday_notify_days=30, line_width=70)
        daily_prompt.birthdays = [
            Birthday('2008-03-01', 'Abacus')
            ]
        msg_re = r'Birthday of Abacus \(15\) in 10 days'
        gs = daily_prompt.get_str(line_width=70, today=date(2023, 2, 19))
        self.assertRegex(gs, msg_re.replace(' ', r'\s+'))

    def testDaysLeapDay(self):
        daily_prompt = DailyPrompt(birthday_notify_days=30, line_width=70)
        daily_prompt.birthdays = [
            Birthday('2008-03-01', 'Abacus')
            ]
        msg_re = r'Birthday of Abacus \(16\) in 12 days'
        gs = daily_prompt.get_str(line_width=70, today=date(2024, 2, 18))
        self.assertRegex(gs, msg_re.replace(' ', r'\s+'))

    def testDaysTomorrow(self):
        daily_prompt = DailyPrompt(birthday_notify_days=30, line_width=70)
        daily_prompt.birthdays = [
            Birthday('2008-08-02', 'Abacus')
            ]
        msg_re = r'Birthday of Abacus \(15\) tomorrow'
        gs = daily_prompt.get_str(line_width=70, today=date(2023, 8, 1))
        self.assertRegex(gs, msg_re.replace(' ', r'\s+'))

    def testDaysToday(self):
        daily_prompt = DailyPrompt(birthday_notify_days=30, line_width=70)
        daily_prompt.birthdays = [
            Birthday('2008-08-01', 'Abacus')
            ]
        msg_re = r'Birthday of Abacus \(15\) today'
        gs = daily_prompt.get_str(line_width=70, today=date(2023, 8, 1))
        self.assertRegex(gs, msg_re.replace(' ', r'\s+'))

    def testTwoPeopleDifferentDays(self):
        daily_prompt = DailyPrompt(birthday_notify_days=30, line_width=70)
        daily_prompt.birthdays = [
            Birthday('2008-08-01', 'Abacus'),
            Birthday('2007-07-31', 'Bacillus')
            ]
        msg_re = r'Birthday of Bacillus \(16\) in 8 days, Abacus \(15\) in 9 days'
        gs = daily_prompt.get_str(line_width=70, today=date(2023, 7, 23))
        self.assertRegex(gs, msg_re.replace(' ', r'\s+'))

    def testThreePeopleDifferentDays(self):
        daily_prompt = DailyPrompt(birthday_notify_days=30, line_width=70)
        daily_prompt.birthdays = [
            Birthday('2008-08-02', 'Abacus'),
            Birthday('2007-08-01', 'Bacillus'),
            Birthday('2006-07-31', 'Cecil')
            ]
        msg_re = r'Birthday of Cecil \(17\) in 8 days, Bacillus \(16\) in 9 days, Abacus \(15\) in 10 days'
        gs = daily_prompt.get_str(line_width=70, today=date(2023, 7, 23))
        self.assertRegex(gs, msg_re.replace(' ', r'\s+'))

    def testTwoPeopleSameDayAlphaAscending(self):
        daily_prompt = DailyPrompt(birthday_notify_days=30, line_width=70)
        daily_prompt.birthdays = [
            Birthday('2007-08-01', 'Bacillus'),
            Birthday('2008-08-01', 'Abacus')
            ]
        msg_re = r'Birthday of Abacus \(15\) and Bacillus \(16\) in 9 days'
        gs = daily_prompt.get_str(line_width=70, today=date(2023, 7, 23))
        self.assertRegex(gs, msg_re.replace(' ', r'\s+'))

    def testThreePeopleSameDayAlphaAscending(self):
        daily_prompt = DailyPrompt(birthday_notify_days=30, line_width=70)
        daily_prompt.birthdays = [
            Birthday('2006-08-01', 'Cecil'),
            Birthday('2008-08-01', 'Abacus'),
            Birthday('2007-08-01', 'Bacillus')
            ]
        msg_re = r'Birthday of Abacus \(15\), Bacillus \(16\) and Cecil \(17\) on Tuesday'
        gs = daily_prompt.get_str(line_width=70, today=date(2023, 7, 26))
        self.assertRegex(gs, msg_re.replace(' ', r'\s+'))


if __name__ == '__main__':
    unittest.main()
