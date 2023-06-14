import unittest

from time_tag_birthday_prompt.time_tag import TimeTag, construct_time_tags

from time_tag_birthday_prompt.exceptions import (
    TimeTagErrorGroup, TimeFieldErrorGroup, IncorrectParameterTypeError,
    IncorrectTimeFormatError, TimeDoesntExistError, TimeOrderError
    )


def assertExceptionInGroup(self, exc_type, err_group):
    found = False
    for err in err_group.exceptions:
        if isinstance(err, exc_type):
            found = True
            break
    self.assertTrue(found)


class TestTimeTagInit(unittest.TestCase):
    """Test `TimeTag` object `__init__()` method."""

    def testIncorrectStartTimeTypeError(self):
        with self.assertRaises(IncorrectParameterTypeError):
            TimeTag((0, 'start'), '15:00', 'text')

    def testIncorrectStopTimeTypeError(self):
        with self.assertRaises(IncorrectParameterTypeError):
            TimeTag('09:00', (0, 'stop'), 'text')

    def testIncorrectTextTypeError(self):
        with self.assertRaises(IncorrectParameterTypeError):
            TimeTag('09:00', '15:00', (0, 'text'))

    def testIncorrectTimeFormatErrorStartNoColon(self):
        with self.assertRaises(TimeFieldErrorGroup) as cm:
            TimeTag('0900', '15:00', 'text')
        assertExceptionInGroup(self, IncorrectTimeFormatError, cm.exception)

    def testIncorrectTimeFormatErrorStartHourAlphabet(self):
        with self.assertRaises(TimeFieldErrorGroup) as cm:
            TimeTag('xx:00', '15:00', 'text')
        assertExceptionInGroup(self, IncorrectTimeFormatError, cm.exception)

    def testIncorrectTimeFormatErrorStartMinuteAlphabet(self):
        with self.assertRaises(TimeFieldErrorGroup) as cm:
            TimeTag('09:xx', '15:00', 'text')
        assertExceptionInGroup(self, IncorrectTimeFormatError, cm.exception)

    def testIncorrectTimeFormatErrorStopNoColon(self):
        with self.assertRaises(TimeFieldErrorGroup) as cm:
            TimeTag('09:00', '1500', 'text')
        assertExceptionInGroup(self, IncorrectTimeFormatError, cm.exception)

    def testIncorrectTimeFormatErrorStopHourAlphabet(self):
        with self.assertRaises(TimeFieldErrorGroup) as cm:
            TimeTag('09:00', 'xx:00', 'text')
        assertExceptionInGroup(self, IncorrectTimeFormatError, cm.exception)

    def testIncorrectTimeFormatErrorStopMinuteAlphabet(self):
        with self.assertRaises(TimeFieldErrorGroup) as cm:
            TimeTag('09:00', '15:xx', 'text')
        assertExceptionInGroup(self, IncorrectTimeFormatError, cm.exception)

    def testTimeDoesntExistErrorStartHour25(self):
        with self.assertRaises(TimeFieldErrorGroup) as cm:
            TimeTag('25:00', '15:00', 'text')
        assertExceptionInGroup(self, TimeDoesntExistError, cm.exception)

    def testTimeDoesntExistErrorStartHourMinusOne(self):
        with self.assertRaises(TimeFieldErrorGroup) as cm:
            TimeTag('-1:00', '15:00', 'text')
        assertExceptionInGroup(self, TimeDoesntExistError, cm.exception)

    def testTimeDoesntExistErrorStartMinute60(self):
        with self.assertRaises(TimeFieldErrorGroup) as cm:
            TimeTag('09:60', '15:00', 'text')
        assertExceptionInGroup(self, TimeDoesntExistError, cm.exception)

    def testTimeDoesntExistErrorStartMinuteMinusOne(self):
        with self.assertRaises(TimeFieldErrorGroup) as cm:
            TimeTag('09:-1', '15:00', 'text')
        assertExceptionInGroup(self, TimeDoesntExistError, cm.exception)

    def testTimeDoesntExistErrorStopHour25(self):
        with self.assertRaises(TimeFieldErrorGroup) as cm:
            TimeTag('09:00', '25:00', 'text')
        assertExceptionInGroup(self, TimeDoesntExistError, cm.exception)

    def testTimeDoesntExistErrorStopHourMinusOne(self):
        with self.assertRaises(TimeFieldErrorGroup) as cm:
            TimeTag('09:00', '-1:00', 'text')
        assertExceptionInGroup(self, TimeDoesntExistError, cm.exception)

    def testTimeDoesntExistErrorStopMinute60(self):
        with self.assertRaises(TimeFieldErrorGroup) as cm:
            TimeTag('09:00', '15:60', 'text')
        assertExceptionInGroup(self, TimeDoesntExistError, cm.exception)

    def testTimeDoesntExistErrorStopMinuteMinusOne(self):
        with self.assertRaises(TimeFieldErrorGroup) as cm:
            TimeTag('09:00', '15:-1', 'text')
        assertExceptionInGroup(self, TimeDoesntExistError, cm.exception)


class TestConstructTimeTags(unittest.TestCase):
    """Test `construct_birthdays()` function."""

    def testTimeTagErrorGroupOneException(self):
        with self.assertRaises(TimeTagErrorGroup) as cm:
            construct_time_tags(
                [((0, 'start'), '15:00', 'text')])
        self.assertEqual(len(cm.exception.exceptions), 1)

    def testTimeTagErrorGroupStillOneException(self):
        with self.assertRaises(TimeTagErrorGroup) as cm:
            construct_time_tags(
                [((0, 'start'), 'xx:00', 'text')])
        self.assertEqual(len(cm.exception.exceptions), 1)

    def testTimeTagErrorGroupTwoExceptions(self):
        with self.assertRaises(TimeTagErrorGroup) as cm:
            construct_time_tags([
                ('09:00', '-1:00', 'text'),
                ('09:00', '15:-1', 'text')
                ])
        self.assertEqual(len(cm.exception.exceptions), 2)

    def testTimeTagErrorGroupThreeExceptions(self):
        with self.assertRaises(TimeTagErrorGroup) as cm:
            construct_time_tags([
                ('09:xx', '15:00', 'text'),
                ('09:xx', '15:00', 'text'),
                ('09:00', (0, 'stop'), 'text')
                ])
        self.assertEqual(len(cm.exception.exceptions), 3)

if __name__ == '__main__':
    unittest.main()
