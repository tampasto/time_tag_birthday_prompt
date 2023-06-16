"""
Define `TimeTag` class and a function `construct_time_tags()` for generating
these objects.

`TimeTag` objects are initiated, stored and used internally by
`PrimaryPrompt`.

"""

from typing import Tuple, List

from .exceptions import (
    TimeTagInitGroup, IncorrectParameterTypeError, IncorrectTimeFormatError,
    TimeDoesntExistError
    )


class TimeTag:
    def __init__(self, start: str, stop: str, text: str):
        self.start = start
        self.stop = stop
        self.text = text
        self.start_tuple: Tuple[int, int]
        self.stop_tuple: Tuple[int, int]

        err_list = []
        if not isinstance(start, str):
            err_list.append(IncorrectParameterTypeError(
                'start', type(start).__name__, 'time tag', text, 'string'))
        else:
            self.start_tuple = self.resolve_tuple('start', self.start, err_list)
        
        if not isinstance(stop, str):
            err_list.append(IncorrectParameterTypeError(
                'stop', type(stop).__name__, 'time tag', text, 'string'))
        else:
            self.stop_tuple = self.resolve_tuple('stop', self.stop, err_list)
        
        if not isinstance(text, str):
            err_list.append(IncorrectParameterTypeError(
                'text', type(text).__name__, 'time tag', expected_type='string'))
        
        if len(err_list) > 0:
            raise TimeTagInitGroup('TimeTagInitGroup', tuple(err_list))
    
    def resolve_tuple(
            self, field_name: str, time_value: str, err_list: List[Exception]
            ) -> Tuple[int] | None:
        sp = time_value.split(':', 1)
        if len(sp) == 1:
            err_list.append(
                IncorrectTimeFormatError(field_name, time_value, self.text))
            return None
        
        try:
            h, m = int(sp[0]), int(sp[1])
        except ValueError:
            err_list.append(
                IncorrectTimeFormatError(field_name, time_value, self.text))
            return None
        
        if h < 0 or h > 23 or m < 0 or m > 59:
            err_list.append(
                TimeDoesntExistError(field_name, time_value, self.text))
            return None
        return h, m
