"""
Define `Birthday` class and a function `get_birthdays()` for generating
these objects.

`Birthday` objects are initiated, stored and used internally by
`DailyPrompt`.

"""

from datetime import date

from .exceptions import (
    BirthdayErrorGroup, IncorrectDateFormatError, NullYearError,
    DateDoesntExistError
    )
import data_birthdays


class Birthday:
    def __init__(self, date_str: str, name: str):
        self.date_str = date_str
        self.name = name
        self.date: date

        date_parts = self.date_str.split('-')
        try:
            date_parts = [int(pt) for pt in date_parts]
        except ValueError:
            raise IncorrectDateFormatError(self.date_str, self.name)
        
        if len(date_parts) == 3:
            if date_parts[0] == date.min.year:
                raise NullYearError(
                    self.date_str, self.name, date.min.year)
        elif len(date_parts) == 2:
            date_parts.insert(0, date.min.year)
        else:
            raise IncorrectDateFormatError(self.date_str, self.name)
        
        try:
            self.date = date(*date_parts)
        except ValueError:
            raise DateDoesntExistError(self.date_str, self.name)


def get_birthdays():
    bdays = []
    err_list = []
    for bday in data_birthdays.BIRTHDAYS:
        try:
            bdays.append(Birthday(*bday))
        except (IncorrectDateFormatError, NullYearError,
                DateDoesntExistError) as err:
            err_list.append(err)
    if len(err_list) > 0:
        raise BirthdayErrorGroup('BirthdayErrorGroup', tuple(err_list))
    return bdays
