"""
Define exceptions of the package.

None of these exceptions are expected to be propagated out of the
classes as sys.ps1 and sys.ps2 do not print raised exceptions. If the
`__str__()` method of a prompt class raises an exception, the prompt
will be empty.

"""

from textwrap import fill


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


class BirthdayErrorGroup(ExceptionGroup):
    pass


class IncorrectDateFormatError(Exception):
    def __init__(self, date_str: str, name: str):
        self.date = date_str
        self.name = name
    
    def __str__(self):
        return (
            f"Incorrect birthday '{self.date}' for '{self.name}'. "
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


class TimeTagErrorGroup(ExceptionGroup):
    pass


class TimeFieldErrorGroup(ExceptionGroup):
    pass


class IncorrectTimeFormatError(Exception):
    def __init__(self, field_name: str, time_value: str, tag_text: str):
        self.field_name = field_name
        self.time_value = time_value
        self.tag_text = tag_text
    
    def __str__(self):
        return (
            f"Incorrect {self.field_name} time value '{self.time_value}' for "
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


class TimeOrderError(Exception):
    def __init__(self, value_start: str, value_stop: str, tag_text: str):
        self.value_start = value_start
        self.value_stop = value_stop
        self.tag_text = tag_text
    
    def __str__(self):
        return (
            f"Start time '{self.value_start}' is after stop time "
            f"'{self.value_stop}' for '{self.tag_text}'."
            )


class LineWidthLessThanOneError(Exception):
    def __init__(self, line_width: int):
        self.line_width = line_width

    def __str__(self):
        return (
            f"Parameter 'line_width' value {self.line_width} is less than one."
            )
