"""
Define `TimeTag` class.

`TimeTag` objects are initiated, stored and used internally by
`PrimaryPrompt`.

"""

from typing import Tuple, List

from .exceptions import (
    TimeTagInitGroup, IncorrectParameterTypeError, IncorrectTimeFormatError,
    TimeDoesntExistError
    )


class TimeTag:
    """
    Class of `TimeTag` objects.

    Initialized from the JSON data.

    Attributes
    ----------
    start
    stop
    text
    start_tuple : Tuple[int, int]
        Tuple of (hours, minutes) resolved from string `start`.
    stop_tuple : Tuple[int, int]
        Tuple of (hours, minutes) resolved from string `stop`.
    """
    def __init__(self, start: str, stop: str, text: str):
        """
        Initialize a `TimeTag` object.

        Parameters
        ----------
        start : str
            Start time in format HH:MM.
        stop : str
            Stop time in format HH:MM.
        text : str
            Tag text printed in front of command line prompt.

        Raises
        ------
        TimeTagInitGroup
            The `ExceptionGroup` may contain errors
            `IncorrectParameterTypeError`, `IncorrectTimeFormatError`
            and/or `TimeDoesntExistError`.
        """
        self.start = start
        """Start time in format HH:MM."""
        self.stop = stop
        """Stop time in format HH:MM."""
        self.text = text
        """Tag text printed in front of command line prompt."""
        self.start_tuple: Tuple[int, int]
        """Tuple of (hours, minutes) resolved from string `start`."""
        self.stop_tuple: Tuple[int, int]
        """Tuple of (hours, minutes) resolved from string `stop`."""

        err_list = []
        if not isinstance(start, str):
            err_list.append(IncorrectParameterTypeError(
                'start', type(start).__name__, 'time tag', text, 'string'))
        else:
            self.start_tuple = self._resolve_tuple('start', self.start, err_list)
        
        if not isinstance(stop, str):
            err_list.append(IncorrectParameterTypeError(
                'stop', type(stop).__name__, 'time tag', text, 'string'))
        else:
            self.stop_tuple = self._resolve_tuple('stop', self.stop, err_list)
        
        if not isinstance(text, str):
            err_list.append(IncorrectParameterTypeError(
                'text', type(text).__name__, 'time tag', expected_type='string'))
        
        if len(err_list) > 0:
            raise TimeTagInitGroup('TimeTagInitGroup', tuple(err_list))
    
    def _resolve_tuple(
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
