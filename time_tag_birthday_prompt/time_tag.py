"""
Define `TimeTag` class and a function `construct_time_tags()` for generating
these objects.

`TimeTag` objects are initiated, stored and used internally by
`PrimaryPrompt`.

"""

from typing import List, Tuple

from .exceptions import (
    TimeTagErrorGroup, TimeFieldErrorGroup, IncorrectParameterTypeError,
    IncorrectTimeFormatError, TimeDoesntExistError, TimeOrderError
    )


class TimeTag:
    def __init__(self, start: str, stop: str, text: str):
        self.start = start
        self.stop = stop
        self.text = text
        self.start_tuple: Tuple[int, int]
        self.stop_tuple: Tuple[int, int]

        if not isinstance(start, str):
            raise IncorrectParameterTypeError(
                'start', type(start).__name__, 'time tag', text, 'string')
        if not isinstance(stop, str):
            raise IncorrectParameterTypeError(
                'stop', type(stop).__name__, 'time tag', text, 'string')
        if not isinstance(text, str):
            raise IncorrectParameterTypeError(
                'text', type(text).__name__, 'time tag', text, 'string')

        err_list = []
        for field_name in ('start', 'stop'):
            field_value = getattr(self, field_name)
            sp = field_value.split(':', 1)
            if len(sp) == 1:
                err_list.append(
                    IncorrectTimeFormatError(
                        field_name, field_value, self.text))
                continue
            try:
                h, m = int(sp[0]), int(sp[1])
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


def construct_time_tags(time_tags: List[Tuple[str, str, str]]) -> List[TimeTag]:
    ttags = []
    err_list = []
    for tag in time_tags:
        try:
            ttags.append(TimeTag(*tag))
        except TimeFieldErrorGroup as err_group:
            for err in err_group.exceptions:
                err_list.append(err)
        except (IncorrectParameterTypeError, TimeOrderError) as err:
            err_list.append(err)
    
    if len(err_list) > 0:
        raise TimeTagErrorGroup('TimeTagErrorGroup', tuple(err_list))
    return ttags
