"""
Define exceptions of the package.

Exceptions are raised out of classes only during class initialization
and only related to `__init__` parameter values. Exceptions related to
corrupt JSON data file will not be propagated out of classes but
displayed in string form in the console. JSON exceptions are gathered
into exception groups when raised.

No exceptions are expected to be raised after initialization. Even if
bugs raised exceptions when `sys.ps1` or `sys.ps2` call `str()` on their
values, the stack trace texts would be suspended and the prompt would be
an empty string.

"""

from typing import Tuple, List


# Exceptions raised on class initialization


class IncorrectParameterTypeError(Exception):
    def __init__(
            self, param_name: str, type_str: str, obj_desc: str,
            rec_name: str | None = None, expected_type: str | None = None
            ) -> None:
        self.param_name = param_name
        self.type_str = type_str
        self.obj_desc = obj_desc
        self.rec_name = rec_name
        self.expected_type = expected_type
    
    def __str__(self):
        text = (
            f"Incorrect '{self.param_name}' parameter type '{self.type_str}' "
            f"for {self.obj_desc}"
            )
        if self.rec_name:
            text += f" '{self.rec_name}'"
        text += '.'
        if self.expected_type:
            text += f' Expected string.'
        return text


class LineWidthLessThanTenError(Exception):
    def __init__(self, line_width: int):
        self.line_width = line_width

    def __str__(self):
        return (
            f"Parameter 'line_width' value {self.line_width} is less than ten."
            )


class BirthdayNotifyDaysLessThanZeroError(Exception):
    def __init__(self, birthday_notify_days: int):
        self.birthday_notify_days = birthday_notify_days

    def __str__(self):
        return (
            "Parameter 'birthday_notify_days' value "
            f'{self.birthday_notify_days} is less than zero.'
            )


# Internally handled JSON exceptions


class DataLoaderInitGroup(ExceptionGroup):
    def __init__(self, path: str, exc_tuple: Tuple[Exception]) -> None:
        super().__init__('DataLoaderInitGroup', exc_tuple)
        self.path = path
    
    def get_messages(self) -> List[str]:
        msg_list = [f'Errors in JSON data file.', f'Path: {self.path}']
        for err in self.exceptions:
            msg_list.append(str(err))
        return msg_list


class CorruptJSONFileError(Exception):
    def __init__(self, msg: str):
        self.msg = msg

    def __str__(self):
        return f'{self.msg}'


class ConstructBirthdaysGroup(ExceptionGroup):
    pass


class BirthdayInitGroup(ExceptionGroup):
    pass


class IncorrectDateFormatError(Exception):
    def __init__(self, date_str: str, name: str):
        self.date = date_str
        self.name = name
    
    def __str__(self):
        return (
            f"Incorrect birthday format '{self.date}' for '{self.name}'. "
            f"Expected YYYY-MM-DD or MM-DD."
            )


class NullYearError(Exception):
    def __init__(self, date_str: str, name: str, null_year: int):
        self.date = date_str
        self.name = name
        self.null_year = null_year
    
    def __str__(self):
        return (
            f"Null year {self.null_year} used in birthday '{self.date}' "
            f"for '{self.name}'."
            )

class DateDoesntExistError(Exception):
    def __init__(self, date_str: str, name: str):
        self.date = date_str
        self.name = name
    
    def __str__(self):
        return (
            f"Incorrect numeric values in birthday '{self.date}' for "
            f"'{self.name}'."
            )


class ConstructTimeTagsGroup(ExceptionGroup):
    pass


class TimeTagInitGroup(ExceptionGroup):
    pass


class IncorrectTimeFormatError(Exception):
    def __init__(self, field_name: str, time_value: str, tag_text: str):
        self.field_name = field_name
        self.time_value = time_value
        self.tag_text = tag_text
    
    def __str__(self):
        return (
            f"Incorrect {self.field_name} time format '{self.time_value}' for "
            f"tag '{self.tag_text}'. Expected HH:MM."
            )


class TimeDoesntExistError(Exception):
    def __init__(self, field_name: str, time_value: str, tag_text: str):
        self.field_name = field_name
        self.time_value = time_value
        self.tag_text = tag_text
    
    def __str__(self):
        return (
            f"Incorrect numeric values in {self.field_name} time "
            f"'{self.time_value}' for '{self.tag_text}'."
            )
