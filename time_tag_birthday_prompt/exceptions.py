"""
Define exceptions of the package.

None of these exceptions are expected to be propagated out of the
classes as sys.ps1 and sys.ps2 do not print raised exceptions. If the
`__str__()` method of a prompt class raises an exception, the prompt
will be empty.

"""

from textwrap import fill


class BirthdayErrorGroup(ExceptionGroup):
    pass


class IncorrectDateTypeError(Exception):
    def __init__(self, type_str: str, name: str):
        self.type_str = type_str
        self.name = name
    
    def __str__(self):
        return (
            f"Incorrect type {self.type_str} of parameter 'date_str' for "
            f"'{self.name}'. Expected a string or datetime.date."
            )

class IncorrectNameTypeError(Exception):
    def __init__(self, type_str: str):
        self.type_str = type_str
    
    def __str__(self):
        return (
            f"Incorrect type for name '{self.type_str}'. Expected a string."
            )

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
    def __init__(self, field_name: str, time_value: str, tag_name: str):
        self.field_name = field_name
        self.time_value = time_value
        self.tag_name = tag_name
    
    def __str__(self):
        return (
            f"Incorrect {self.field_name} time value '{self.time_value}' for "
            f"tag '{self.tag_name}'. Expected HH:MM."
            )


class TimeDoesntExistError(Exception):
    def __init__(self, field_name: str, time_value: str, tag_name: str):
        self.field_name = field_name
        self.time_value = time_value
        self.tag_name = tag_name
    
    def __str__(self):
        return (
            f"Incorrect numeric values in {self.field_name} time "
            f"'{self.time_value}' for '{self.tag_name}'."
            )


class TimeOrderError(Exception):
    def __init__(self, value_start: str, value_stop: str, tag_name: str):
        self.value_start = value_start
        self.value_stop = value_stop
        self.tag_name = tag_name
    
    def __str__(self):
        return (
            f"Start time '{self.value_start}' is after stop time "
            f"'{self.value_stop}' for '{self.tag_name}'."
            )


class IncorrectReferenceError(Exception):
    def __init__(self, parameter_name: str, arg_type: object):
        self.parameter_name = parameter_name
        self.arg_type = arg_type
