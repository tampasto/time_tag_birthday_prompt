import unittest

from time_tag_birthday_prompt.time_tag import TimeTag

from time_tag_birthday_prompt.exceptions import (
    TimeTagInitGroup, IncorrectParameterTypeError,
    IncorrectTimeFormatError, TimeDoesntExistError
    )


def assertExceptionInGroup(
        self, exc_type, err_group: ExceptionGroup) -> bool:
    found = False
    for err in err_group.exceptions:
        if isinstance(err, exc_type):
            found = True
            break
    self.assertTrue(found)


class TestTimeTag__init__(unittest.TestCase):
    """Test `TimeTag` object `__init__()` method."""

    def testParam_start_incorrectType(self):
        with self.assertRaises(TimeTagInitGroup) as cm:
            TimeTag((0, 'start'), '15:00', 'text')
        assertExceptionInGroup(self, IncorrectParameterTypeError, cm.exception)

    def testParam_stop_incorrectType(self):
        with self.assertRaises(TimeTagInitGroup) as cm:
            TimeTag('09:00', (0, 'stop'), 'text')
        assertExceptionInGroup(self, IncorrectParameterTypeError, cm.exception)

    def testParam_text_incorrectType(self):
        with self.assertRaises(TimeTagInitGroup) as cm:
            TimeTag('09:00', '15:00', (0, 'text'))
        assertExceptionInGroup(self, IncorrectParameterTypeError, cm.exception)

    def testParam_start_IncorrectTimeFormatError_noColon(self):
        with self.assertRaises(TimeTagInitGroup) as cm:
            TimeTag('0900', '15:00', 'text')
        assertExceptionInGroup(self, IncorrectTimeFormatError, cm.exception)

    def testParam_start_IncorrectTimeFormatError_hourAlphabet(self):
        with self.assertRaises(TimeTagInitGroup) as cm:
            TimeTag('xx:00', '15:00', 'text')
        assertExceptionInGroup(self, IncorrectTimeFormatError, cm.exception)

    def testParam_start_IncorrectTimeFormatError_minuteAlphabet(self):
        with self.assertRaises(TimeTagInitGroup) as cm:
            TimeTag('09:xx', '15:00', 'text')
        assertExceptionInGroup(self, IncorrectTimeFormatError, cm.exception)

    def testParam_stop_IncorrectTimeFormatError_noColon(self):
        with self.assertRaises(TimeTagInitGroup) as cm:
            TimeTag('09:00', '1500', 'text')
        assertExceptionInGroup(self, IncorrectTimeFormatError, cm.exception)

    def testParam_stop_IncorrectTimeFormatError_hourAlphabet(self):
        with self.assertRaises(TimeTagInitGroup) as cm:
            TimeTag('09:00', 'xx:00', 'text')
        assertExceptionInGroup(self, IncorrectTimeFormatError, cm.exception)

    def testParam_stop_IncorrectTimeFormatError_minuteAlphabet(self):
        with self.assertRaises(TimeTagInitGroup) as cm:
            TimeTag('09:00', '15:xx', 'text')
        assertExceptionInGroup(self, IncorrectTimeFormatError, cm.exception)

    def testParam_start_TimeDoesntExistError_hour25(self):
        with self.assertRaises(TimeTagInitGroup) as cm:
            TimeTag('25:00', '15:00', 'text')
        assertExceptionInGroup(self, TimeDoesntExistError, cm.exception)

    def testParam_start_TimeDoesntExistError_hourMinusOne(self):
        with self.assertRaises(TimeTagInitGroup) as cm:
            TimeTag('-1:00', '15:00', 'text')
        assertExceptionInGroup(self, TimeDoesntExistError, cm.exception)

    def testParam_start_TimeDoesntExistError_minute60(self):
        with self.assertRaises(TimeTagInitGroup) as cm:
            TimeTag('09:60', '15:00', 'text')
        assertExceptionInGroup(self, TimeDoesntExistError, cm.exception)

    def testParam_start_TimeDoesntExistError_minuteMinusOne(self):
        with self.assertRaises(TimeTagInitGroup) as cm:
            TimeTag('09:-1', '15:00', 'text')
        assertExceptionInGroup(self, TimeDoesntExistError, cm.exception)

    def testParam_stop_TimeDoesntExistError_hour25(self):
        with self.assertRaises(TimeTagInitGroup) as cm:
            TimeTag('09:00', '25:00', 'text')
        assertExceptionInGroup(self, TimeDoesntExistError, cm.exception)

    def testParam_stop_TimeDoesntExistError_hourMinusOne(self):
        with self.assertRaises(TimeTagInitGroup) as cm:
            TimeTag('09:00', '-1:00', 'text')
        assertExceptionInGroup(self, TimeDoesntExistError, cm.exception)

    def testParam_stop_TimeDoesntExistError_minute60(self):
        with self.assertRaises(TimeTagInitGroup) as cm:
            TimeTag('09:00', '15:60', 'text')
        assertExceptionInGroup(self, TimeDoesntExistError, cm.exception)

    def testParam_stop_TimeDoesntExistError_minuteMinusOne(self):
        with self.assertRaises(TimeTagInitGroup) as cm:
            TimeTag('09:00', '15:-1', 'text')
        assertExceptionInGroup(self, TimeDoesntExistError, cm.exception)


if __name__ == '__main__':
    unittest.main()
