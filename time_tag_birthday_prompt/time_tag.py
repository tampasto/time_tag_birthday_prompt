"""
Define `TimeTag` class and a function `get_time_tags()` for generating
these objects.

`TimeTag` objects are initiated, stored and used internally by
`PrimaryPrompt`.

"""

from typing import List, Tuple

from data_time_tags import TIME_TAGS
from .exceptions import (
    TimeTagErrorGroup, TimeFieldErrorGroup, IncorrectTimeFormatError,
    TimeDoesntExistError, TimeOrderError
    )


class TimeTag:
    def __init__(self, start: str, stop: str, text: str):
        self.start = start
        self.stop = stop
        self.text = text
        self.start_tuple: Tuple[int, int]
        self.stop_tuple: Tuple[int, int]

        err_list = []
        for field_name in ('start', 'stop'):
            field_value = getattr(self, field_name)
            h, m = field_value.split(':', 1)
            try:
                h, m = int(h), int(m)
            except ValueError:
                err_list.append(
                    IncorrectTimeFormatError(
                        field_name, field_value, self.text))
            else:
                setattr(self, f'{field_name}_tuple', (h, m))
                
                if h < 0 or h > 23 or m < 0 or m > 59:
                    err_list.append(
                        TimeDoesntExistError(field_name, field_value, self.text))
        
        if len(err_list) > 0:
            raise TimeFieldErrorGroup('TimeFieldErrorGroup', tuple(err_list))
        
        if self.start_tuple > self.stop_tuple and self.stop_tuple != (0, 0):
            raise TimeOrderError(self.start_tuple, self.stop_tuple, self.text)


def get_time_tags() -> List[TimeTag]:
    time_tags = []
    err_list = []
    for tag in TIME_TAGS:
        try:
            time_tags.append(TimeTag(*tag))
        except TimeFieldErrorGroup as err_group:
            for err in err_group.exceptions:
                err_list.append(err)
        except TimeOrderError as err:
            err_list.append(err)
    
    if len(err_list) > 0:
        raise TimeTagErrorGroup('TimeTagErrorGroup', tuple(err_list))
    return time_tags
