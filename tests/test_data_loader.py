from tempfile import TemporaryFile
from typing import List
import unittest

from time_tag_birthday_prompt.data_loader import DataLoader

from .extend_unittest import assertGroupMatchesExceptions
from time_tag_birthday_prompt.exceptions import (
    ConstructBirthdaysGroup, ConstructTimeTagsGroup, DataLoaderInitGroup,
    IncorrectDateFormatError, DateDoesntExistError, TimeDoesntExistError,
    IncorrectTimeFormatError
    )


def assertMethodRaisesGroup(
        self: unittest.TestCase, file_txt: str, exc_type_list: List,
        method_name: str, group_type: object
        ) -> None:
    dl = None
    with TemporaryFile(mode='w+', encoding='utf-8') as tf:
        tf.write(file_txt)
        tf.seek(0)
        dl = DataLoader(tf, '<testing>')

    method_callable = getattr(dl, method_name)
    with self.assertRaises(group_type) as cm:
        method_callable()
    assertGroupMatchesExceptions(self, cm.exception, exc_type_list)


class TestDataLoader__init__(unittest.TestCase):
    """Test `DataLoader` object `__init__()` method."""
    
    def matchCorruptJSONFileErrorMsg(self, file_txt: str, err_msgs: List[str]):
        err_group = None
        with TemporaryFile(mode='w+', encoding='utf-8') as tf:
            tf.write(file_txt)
            tf.seek(0)
            if len(err_msgs) > 0:
                with self.assertRaises(DataLoaderInitGroup) as cm:
                    DataLoader(tf, '<testing>')
                err_group = cm.exception
            else:
                try:
                    DataLoader(tf, '<testing>')
                except DataLoaderInitGroup as dl_group:
                    unexpected_msgs = [
                        err.msg for err in dl_group.exceptions]
                    self.fail(f'Unexpected message(s) {unexpected_msgs!r}, expected no messages')
                return
        
        unexpected_msgs = []
        for err in err_group.exceptions:
            if err.msg in err_msgs:
                err_msgs.remove(err.msg)
            else:
                unexpected_msgs.append(err.msg)
        if len(unexpected_msgs) > 0 or len(err_msgs) > 0:
            self.fail(f'Unexpected message(s) {unexpected_msgs!r}, lacking message(s) {err_msgs!r}')

    def testJSON_CorruptJSONFileError_JSONDecodeError(self):
        is_found = False
        with TemporaryFile(mode='w+', encoding='utf-8') as tf:
            tf.write(r'{"timeTags: []}')
            tf.seek(0)
            with self.assertRaises(DataLoaderInitGroup) as cm:
                DataLoader(tf, '<testing>')
            for err in cm.exception.exceptions:
                if 'Corrupt JSON on row' in str(err):
                    is_found = True
                    break
        self.assertTrue(is_found)

    def testJSON_CorruptJSONFileError_birthdayMissing(self):
        self.matchCorruptJSONFileErrorMsg(
            r'{"timeTags": []}',
            ["Field 'birthdays' missing from root."]
            )

    def testJSON_CorruptJSONFileError_timeTagsMissing(self):
        self.matchCorruptJSONFileErrorMsg(
            r'{"birthdays": []}',
            ["Field 'timeTags' missing from root."]
            )

    def testJSON_CorruptJSONFileError_birthdayAndTimeTagsMissing(self):
        self.matchCorruptJSONFileErrorMsg(
            r'{}',
            ["Field 'birthdays' missing from root.",
             "Field 'timeTags' missing from root."]
            )

    def testJSON_CorruptJSONFileError_birthdayAsStr(self):
        self.matchCorruptJSONFileErrorMsg(
            r'{"birthdays": "birthdays", "timeTags": []}',
            ["Field 'birthdays' is not of type array or null."]
            )

    def testJSON_CorruptJSONFileError_timeTagsAsStr(self):
        self.matchCorruptJSONFileErrorMsg(
            r'{"birthdays": [], "timeTags": "timeTags"}',
            ["Field 'timeTags' is not of type array or null."]
            )

    def testJSON_birthdayAndTimeTagsAsEmptyArray(self):
        self.matchCorruptJSONFileErrorMsg(
            r'{"birthdays": [], "timeTags": []}',
            []
            )

    def testJSON_birthdayAsNullAndTimeTagsAsArray(self):
        self.matchCorruptJSONFileErrorMsg(
            r'{"birthdays": null, "timeTags": []}',
            []
            )

    def testJSON_birthdayAsArrayAndTimeTagsAsNull(self):
        self.matchCorruptJSONFileErrorMsg(
            r'{"birthdays": [], "timeTags": null}',
            []
            )

    def testJSON_birthdayAndTimeTagsAsNull(self):
        self.matchCorruptJSONFileErrorMsg(
            r'{"birthdays": null, "timeTags": null}',
            []
            )

    def testJSON_CorruptJSONFileError_birthdayRecAsStr(self):
        self.matchCorruptJSONFileErrorMsg(
            r'{"birthdays": [["", ""], "", ["", ""]], "timeTags": null}',
            ["Array 'birthdays' index 1 is not an array."]
            )

    def testJSON_CorruptJSONFileError_birthdayWith4Items(self):
        self.matchCorruptJSONFileErrorMsg(
            r'{"birthdays": [["", ""], ["", "", ""]], "timeTags": null}',
            ["Array 'birthdays' index 1 length is not 2."]
            )

    def testJSON_CorruptJSONFileError_birthdayDateAsInt(self):
        self.matchCorruptJSONFileErrorMsg(
            r'{"birthdays": [["", ""], ["", ""], [5, "nm"]], "timeTags": null}',
            ["Array 'birthdays' index 2 (name 'nm') field[0] birthday date is not a string."]
            )

    def testJSON_CorruptJSONFileError_birthdayDateAsIntNameAsNull(self):
        self.matchCorruptJSONFileErrorMsg(
            r'{"birthdays": [["", ""], [5, null], ["", ""]], "timeTags": null}',
            ["Array 'birthdays' index 1 (name None) field[0] birthday date is not a string.",
             "Array 'birthdays' index 1 field[1] name is not a string."]
            )

    def testJSON_CorruptJSONFileError_timeTagsAsStr(self):
        self.matchCorruptJSONFileErrorMsg(
            r'{"timeTags": [["", "", ""], ["", "", ""], ""], "birthdays": null}',
            ["Array 'timeTags' index 2 is not an array."]
            )

    def testJSON_CorruptJSONFileError_timeTagsWith3Items(self):
        self.matchCorruptJSONFileErrorMsg(
            r'{"timeTags": [["", "", ""], ["", ""]], "birthdays": null}',
            ["Array 'timeTags' index 1 length is not 3."]
            )

    def testJSON_CorruptJSONFileError_timeTagsStartTimeAsArray(self):
        self.matchCorruptJSONFileErrorMsg(
            r'{"timeTags": [["", "", ""], ["", "", ""], [[1, 2], "", "tx"]], "birthdays": null}',
            ["Array 'timeTags' index 2 (text 'tx') field[0] start time is not a string."]
            )

    def testJSON_CorruptJSONFileError_timeTagsEndTimeAsNull(self):
        self.matchCorruptJSONFileErrorMsg(
            r'{"timeTags": [["", null, "tx"], ["", "", ""], ["", "", ""]], "birthdays": null}',
            ["Array 'timeTags' index 0 (text 'tx') field[1] stop time is not a string."]
            )

    def testJSON_CorruptJSONFileError_timeTagsTextAsObject(self):
        self.matchCorruptJSONFileErrorMsg(
            r'{"timeTags": [["", "", ""], ["", "", ""], ["", "", {"a": 1}]], "birthdays": null}',
            ["Array 'timeTags' index 2 field[2] text is not a string."]
            )


class TestDataLoader_construct_birthdays(unittest.TestCase):
    """Test `DataLoader` object `construct_birthdays()` method."""

    def assertConstructBirthdaysRaisesGroup(
            self, birthdays_array_txt: str, exc_type_list: List):
        assertMethodRaisesGroup(
            self,
            '{"birthdays": [' + birthdays_array_txt + '], "timeTags": null}',
            exc_type_list,
            'construct_birthdays',
            ConstructBirthdaysGroup
            )

    def test_ConstructBirthdaysGroup_oneException(self):
        self.assertConstructBirthdaysRaisesGroup(
            '["191x-01-01", "name"]',
            [IncorrectDateFormatError]
            )

    def test_ConstructBirthdaysGroup_twoExceptionsOnTwo(self):
        self.assertConstructBirthdaysRaisesGroup(
            '["191x-01-01", ""], '
            '["false", "name"]',
            [IncorrectDateFormatError, IncorrectDateFormatError]
            )

    def test_ConstructBirthdaysGroup_threeExceptionsOnThree(self):
        self.assertConstructBirthdaysRaisesGroup(
            '["191x-01-01", ""], '
            '["2023, 6, 1", ""], '
            '["2023-01-61", "name"]',
            [IncorrectDateFormatError, IncorrectDateFormatError,
             DateDoesntExistError]
            )


class TestDataLoader_construct_time_tags(unittest.TestCase):
    """Test `DataLoader` object `construct_time_tags()` method."""

    def assertConstructTimeTagsRaisesGroup(
            self, time_tags_array_txt: str, exc_type_list: List):
        assertMethodRaisesGroup(
            self,
            '{"timeTags": [' + time_tags_array_txt + '], "birthdays": null}',
            exc_type_list,
            'construct_time_tags',
            ConstructTimeTagsGroup
            )

    def test_ConstructTimeTagsGroup_oneException(self):
        self.assertConstructTimeTagsRaisesGroup(
            '["start", "15:00", "text"]',
            [IncorrectTimeFormatError]
            )

    def test_ConstructTimeTagsGroup_twoExceptionsOnOne(self):
        self.assertConstructTimeTagsRaisesGroup(
            '["start", "xx:00", "text"]',
            [IncorrectTimeFormatError, IncorrectTimeFormatError]
            )

    def test_ConstructTimeTagsGroup_twoExceptionsOnTwo(self):
        self.assertConstructTimeTagsRaisesGroup(
            '["09:00", "-1:00", "text"], '
            '["09:00", "15:-1", "text"]',
            [TimeDoesntExistError, TimeDoesntExistError]
            )

    def test_ConstructTimeTagsGroup_threeExceptionsOnTwo(self):
        self.assertConstructTimeTagsRaisesGroup(
            '["09:xx", "15:00", "text"], '
            '["09:00", "15:00", "text"], '
            '["09:65", "25:00", "123"]',
            [IncorrectTimeFormatError, TimeDoesntExistError,
             TimeDoesntExistError]
            )


if __name__ == '__main__':
    unittest.main()
