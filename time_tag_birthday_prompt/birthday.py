"""
Define `Birthday` class.

`Birthday` objects are initiated, stored and used internally by
`BirthdayNotifier`.

"""

from typing import List
import datetime

from .exceptions import (
    BirthdayInitGroup, IncorrectParameterTypeError, IncorrectDateFormatError,
    NullYearError, DateDoesntExistError
    )


class Birthday:
    """
    Class of `Birthday` objects.

    Initialized from the JSON data.

    Attributes
    ----------
    date
    name
    date_obj : datetime.date
        Resolved date based on string `date`.
    """
    def __init__(self, date: str, name: str):
        """
        Initialize a `Birthday` object.

        Parameters
        ----------
        date : str
            Date in format YYYY-MM-DD or MM-DD.
        name : str
            Name of the person or thing having a birthday.

        Raises
        ------
        BirthdayInitGroup
            The `ExceptionGroup` may contain errors
            `IncorrectParameterTypeError`, `IncorrectDateFormatError`,
            `NullYearError` and/or `DateDoesntExistError`.
        """
        self.date = date
        self.name = name
        self.date_obj: datetime.date

        err_list = []
        if not isinstance(date, str):
            err_list.append(IncorrectParameterTypeError(
                'date', type(date).__name__, 'birthday', name, 'string or datetime.date'))
        else:
            self.date_obj = self._resolve_date_obj(err_list)
        
        if not isinstance(name, str):
            err_list.append(IncorrectParameterTypeError(
                'name', type(name).__name__, 'birthday', expected_type='string'))
        
        if len(err_list) > 0:
            raise BirthdayInitGroup('BirthdayInitGroup', tuple(err_list))
    
    def _resolve_date_obj(
            self, err_list: List[Exception]) -> datetime.date | None:
        date_parts = self.date.split('-', 2)
        try:
            date_parts = [int(pt) for pt in date_parts]
        except ValueError:
            err_list.append(IncorrectDateFormatError(self.date, self.name))
            return None
        
        if len(date_parts) == 3:
            if date_parts[0] == datetime.date.min.year:
                err_list.append(
                    NullYearError(
                        self.date, self.name, datetime.date.min.year))
                return None
        elif len(date_parts) == 2:
            date_parts.insert(0, datetime.date.min.year)
        else:
            err_list.append(IncorrectDateFormatError(self.date, self.name))
            return None
        
        date_obj = None
        try:
            date_obj = datetime.date(*date_parts)
        except ValueError:
            err_list.append(DateDoesntExistError(self.date, self.name))
            return None
        else:
            return date_obj
