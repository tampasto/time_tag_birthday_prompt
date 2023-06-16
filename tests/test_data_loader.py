from datetime import date
from tempfile import TemporaryFile
from typing import List
import unittest

from time_tag_birthday_prompt.data_loader import DataLoader

from time_tag_birthday_prompt.exceptions import (
    ConstructBirthdaysGroup, ConstructTimeTagsGroup, CorruptJSONFileError,
    IncorrectDateFormatError, IncorrectParameterTypeError,
    DateDoesntExistError, TimeDoesntExistError, IncorrectTimeFormatError
    )


class TestDataLoaderInit(unittest.TestCase):
    """Test `DataLoader` object `__init__()` method."""
    
    def matchExcText(self, file_txt: str, txt: str):
        tf = TemporaryFile(mode='w+', encoding='utf-8')
        tf.write(file_txt)
        tf.seek(0)
        with self.assertRaises(CorruptJSONFileError) as cm:
            DataLoader(tf, '<testing>')
        tf.close()
        self.assertEqual(cm.exception.msg, txt)

    def testCorruptJSONFileErrorBirthdayMissing(self):
        self.matchExcText(
            r'{"timeTags": []}',
            "Either or both of fields 'birthdays' and 'timeTags' missing from root."
            )

    def testCorruptJSONFileErrorTimeTagsMissing(self):
        self.matchExcText(
            r'{"birthdays": []}',
            "Either or both of fields 'birthdays' and 'timeTags' missing from root."
            )

    def testCorruptJSONFileErrorBirthdayAndTimeTagsMissing(self):
        self.matchExcText(
            r'{}',
            "Either or both of fields 'birthdays' and 'timeTags' missing from root."
            )

    def testCorruptJSONFileErrorBirthdayAsStr(self):
        self.matchExcText(
            r'{"birthdays": "birthdays", "timeTags": []}',
            "Either or both of fields 'birthdays' and 'timeTags' are not of type array or null."
            )

    def testCorruptJSONFileErrorTimeTagsAsStr(self):
        self.matchExcText(
            r'{"birthdays": [], "timeTags": "timeTags"}',
            "Either or both of fields 'birthdays' and 'timeTags' are not of type array or null."
            )

    @unittest.expectedFailure
    def testBirthdayAndTimeTagsAsArray(self):
        self.matchExcText(
            r'{"birthdays": [], "timeTags": []}',
            "Either or both of fields 'birthdays' and 'timeTags' are not of type array or null."
            )

    @unittest.expectedFailure
    def testBirthdayAsNullAndTimeTagsAsArray(self):
        self.matchExcText(
            r'{"birthdays": null, "timeTags": []}',
            "Either or both of fields 'birthdays' and 'timeTags' are not of type array or null."
            )

    @unittest.expectedFailure
    def testBirthdayAsArrayAndTimeTagsAsNull(self):
        self.matchExcText(
            r'{"birthdays": [], "timeTags": null}',
            "Either or both of fields 'birthdays' and 'timeTags' are not of type array or null."
            )

    @unittest.expectedFailure
    def testBirthdayAndTimeTagsAsNull(self):
        self.matchExcText(
            r'{"birthdays": null, "timeTags": null}',
            "Either or both of fields 'birthdays' and 'timeTags' are not of type array or null."
            )

    def testCorruptJSONFileErrorBirthdayAsStr(self):
        self.matchExcText(
            r'{"birthdays": [["", ""], "", ["", ""]], "timeTags": null}',
            "Array 'birthdays' index 1 is not an array."
            )

    def testCorruptJSONFileErrorBirthdayWith4Items(self):
        self.matchExcText(
            r'{"birthdays": [["", ""], ["", "", ""]], "timeTags": null}',
            "Array 'birthdays' index 1 length is not 2."
            )

    def testCorruptJSONFileErrorBirthdayDateAsInteger(self):
        self.matchExcText(
            r'{"birthdays": [["", ""], ["", ""], [5, "nm"]], "timeTags": null}',
            "Array 'birthdays' index 2 \(name nm\) field\[0\] birthday date is not a string."
            )

    def testCorruptJSONFileErrorBirthdayNameAsNull(self):
        self.matchExcText(
            r'{"birthdays": [["", ""], [5, null], ["", ""]], "timeTags": null}',
            "Array 'birthdays' index 1 field\[1\] name is not a string."
            )

    def testCorruptJSONFileErrorTimeTagsAsStr(self):
        self.matchExcText(
            r'{"timeTags": [["", "", ""], ["", "", ""], ""], "birthdays": null}',
            "Array 'timeTags' index 2 is not an array."
            )

    def testCorruptJSONFileErrorTimeTagsWith3Items(self):
        self.matchExcText(
            r'{"timeTags": [["", "", ""], ["", ""]], "birthdays": null}',
            "Array 'timeTags' index 0 length is not 3."
            )

    def testCorruptJSONFileErrorTimeTagsStartTimeAsArray(self):
        self.matchExcText(
            r'{"timeTags": [["", "", ""], ["", "", ""], [[1, 2], "", "tx"]], "birthdays": null}',
            "Array 'timeTags' index 2 \(text tx\) field\[0\] start time is not a string."
            )

    def testCorruptJSONFileErrorTimeTagsEndTimeAsNull(self):
        self.matchExcText(
            r'{"timeTags": [["", null, "tx"], ["", "", ""], ["", "", ""]], "birthdays": null}',
            "Array 'timeTags' index 0 \(text tx\) field\[1\] stop time is not a string."
            )

    def testCorruptJSONFileErrorTimeTagsTextAsObject(self):
        self.matchExcText(
            r'{"timeTags": [["", "", ""], ["", "", ""], ["", "", {"a": 1}]], "birthdays": null}',
            "Array 'timeTags' index 2 field\[2\] text is not a string."
            )


class TestConstructBirthdays(unittest.TestCase):
    """Test `construct_birthdays()` method."""
    
    def matchExcTypeList(self, file_txt: str, exc_type_list: List):
        tf = TemporaryFile(mode='w+', encoding='utf-8')
        tf.write(file_txt)
        tf.seek(0)
        dl = DataLoader(tf, '<testing>')
        with self.assertRaises(ConstructBirthdaysGroup) as cm:
            dl.construct_birthdays()
        tf.close()
        for exc in cm.exception.exceptions:
            is_found = False
            for exc_type in exc_type_list:
                if isinstance(exc, exc_type):
                    exc_type_list.remove(exc_type)
                    is_found = True
                    break
            self.assertTrue(is_found)
        self.assertEqual(len(exc_type_list), 0)

    def testBirthdayErrorGroupOneException(self):
        self.matchExcTypeList(
            r'{"birthdays": [["191x-01-01", "name"]], "timeTags": null}',
            [IncorrectDateFormatError]
            )

    def testBirthdayErrorGroupStillOneException(self):
        self.matchExcTypeList(
            r'{"birthdays": [["191x-01-01", 1]], "timeTags": null}',
            [IncorrectDateFormatError]
            )

    def testBirthdayErrorGroupTwoExceptions(self):
        self.matchExcTypeList(
            r'{"birthdays": [["191x-01-01", 1], [false, "name"]], '
            r'"timeTags": null}',
            [IncorrectDateFormatError, IncorrectParameterTypeError]
            )

    def testBirthdayErrorGroupThreeExceptions(self):
        self.matchExcTypeList(
            r'{"birthdays": [["191x-01-01", 1], [[2023, 6, 1], []], '
            r'["2023-01-61", "name"]], "timeTags": null}',
            [IncorrectDateFormatError, IncorrectParameterTypeError,
             DateDoesntExistError]
            )


class TestConstructTimeTags(unittest.TestCase):
    """Test `construct_time_tags()` method."""
    
    def matchExcTypeList(self, file_txt: str, exc_type_list: List):
        tf = TemporaryFile(mode='w+', encoding='utf-8')
        tf.write(file_txt)
        tf.seek(0)
        dl = DataLoader(tf, '<testing>')
        with self.assertRaises(ConstructTimeTagsGroup) as cm:
            dl.construct_time_tags()
        tf.close()
        self.assertEqual(len(exc_type_list), len(cm.exception.exceptions))
        for exc_i, exc in enumerate(cm.exception.exceptions):
            if not isinstance(exc, exc_type_list[exc_i]):
                self.fail(
                    f'Exc class {exc.__class__.__name__} is '
                    f'not {exc_type_list[exc_i].__name__}'
                    )

    def testTimeTagErrorGroupOneException(self):
        self.matchExcTypeList(
            r'{"timeTags": [[[0, "start"], "15:00", "text"]], "birthdays": null}',
            [IncorrectParameterTypeError]
            )

    def testTimeTagErrorGroupStillOneException(self):
        self.matchExcTypeList(
            r'{"timeTags": [[[0, "start"], "xx:00", "text"]], "birthdays": null}',
            [IncorrectParameterTypeError]
            )

    def testTimeTagErrorGroupTwoExceptions(self):
        self.matchExcTypeList(
            r'{"timeTags": [["09:00", "-1:00", "text"], '
            r'["09:00", "15:-1", "text"]], "birthdays": null}',
            [TimeDoesntExistError, TimeDoesntExistError]
            )

    def testTimeTagErrorGroupTwoExceptions(self):
        self.matchExcTypeList(
            r'{"timeTags": ['
                r'["09:xx", "15:00", "text"], '
                r'["09:xx", "15:00", "text"], '
                r'["09:00", [0, "stop"], "text"]'
            r'], "birthdays": null}',
            [IncorrectTimeFormatError, IncorrectTimeFormatError,
             IncorrectParameterTypeError]
            )


if __name__ == '__main__':
    unittest.main()
