"""
Define `Birthday` class and a function `construct_birthdays()` for generating
these objects.

`Birthday` objects are initiated, stored and used internally by
`DailyPrompt`.

"""

from typing import List, Tuple
import datetime

from .exceptions import (
    BirthdayErrorGroup, IncorrectDateTypeError, IncorrectNameTypeError,
    IncorrectDateFormatError, NullYearError, DateDoesntExistError
    )


class Birthday:
    def __init__(self, date: str | datetime.date, name: str):
        self.date = date
        self.name = name
        self.date_obj: datetime.date

        if isinstance(date, datetime.date):
            self.date_obj = date
        elif not isinstance(date, str):
            raise IncorrectDateTypeError(type(date).__name__, name)
        
        if not isinstance(name, str):
            raise IncorrectNameTypeError(type(name).__name__)
        
        date_parts = self.date.split('-')
        try:
            date_parts = [int(pt) for pt in date_parts]
        except ValueError:
            raise IncorrectDateFormatError(self.date, self.name)
        
        if len(date_parts) == 3:
            if date_parts[0] == datetime.date.min.year:
                raise NullYearError(
                    self.date, self.name, datetime.date.min.year)
        elif len(date_parts) == 2:
            date_parts.insert(0, datetime.date.min.year)
        else:
            raise IncorrectDateFormatError(self.date, self.name)
        
        try:
            self.date_obj = datetime.date(*date_parts)
        except ValueError:
            raise DateDoesntExistError(self.date, self.name)


def construct_birthdays(birthdays: List[Tuple[str, str]]) -> List[Birthday]:
    bdays = []
    err_list = []
    for bday in birthdays:
        try:
            bdays.append(Birthday(*bday))
        except (IncorrectDateTypeError, IncorrectNameTypeError,
                IncorrectDateFormatError, NullYearError, DateDoesntExistError
                ) as err:
            err_list.append(err)
    if len(err_list) > 0:
        raise BirthdayErrorGroup('BirthdayErrorGroup', tuple(err_list))
    return bdays
