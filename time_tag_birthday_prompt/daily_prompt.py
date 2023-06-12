"""
Define `DailyPrompt` class.

The method `__str__()` defines the output of the object.

"""

from datetime import datetime, date
from typing import List
import collections
import textwrap

from .birthday import Birthday, get_birthdays
from .exceptions import BirthdayErrorGroup, format_errors


class DailyPrompt:
    """
    Class for printing weekdays and birthday reminders on REPL startup.
    
    Attributes
    ----------
    birthday_notify_days
    line_width
    """
    _BDTuple = collections.namedtuple('_BDTuple', ['date', 'name'])
    _Proximity = collections.namedtuple('_Proximity', [
        'days_until', 'name', 'bd_age', 'weekday_desc'])
    _WEEKDAYS = [
        'Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday', 'Saturday',
        'Sunday'
        ]

    _NULL_YEAR = 1900

    def __init__(
            self,
            birthday_notify_days: int = 30,
            line_width: int = 70,
            print_on_init: bool = True
            ) -> None:
        """
        Initialize a daily prompt object.
        
        Parameters
        ----------
        birthday_notify_days : int, default 30
            How many days before the birthday a notification is shown.
        line_width : int, default 70
            How many characters fit on one line.
        print_on_init : bool, default True
            If True, print the daily prompt on initialization.
        """
        self.birthday_notify_days: int = birthday_notify_days
        self.line_width: int = line_width

        self._BIRTHDAYS: List[Birthday]
        self._birthday_error_text: str | None = None

        try:
            self._BIRTHDAYS = get_birthdays()
        except BirthdayErrorGroup as err_group:
            self._birthday_error_text = format_errors(err_group)
        
        if print_on_init:
            print(self)
    
    def time_machine(self, date_string: str) -> None:
        """
        Print the daily prompt from another time.
        
        Please be aware of not violating causality.
        
        Parameters
        ----------
        date_string : str
            Your destination time in format YYYY-MM-DD.
        """
        dt = datetime.strptime(date_string, '%Y-%m-%d')
        d = date(dt.year, dt.month, dt.day)
        print(self._get_str(d))
    
    def __str__(self) -> str:
        return self._get_str(date.today())
    
    def _get_str(self, today: date) -> str:
        ret_str = ''
        if self._birthday_error_text:
            ret_str += f'\n{self._birthday_error_text}\n'
        ret_str += (
            '\n' + self.line_width * '-' + '\n'
            + self._format_date(today)
            )
        if not self._birthday_error_text:
            ret_str += self._format_birthday(today)
        ret_str += self.line_width * '-'
        return ret_str
    
    def _format_date(self, today: date) -> str:
        d_str = datetime(today.year, today.month, today.day).strftime(
            '%A, %Y-%m-%d')
        return f'Today is {d_str}\n'
    
    def _format_birthday(self, today: date) -> str:
        prox_list = self._get_proximity_list(today)
        prox_list.sort()
        bday_string = self._format_proximity_list(prox_list)
        if bday_string is not None:
            return textwrap.fill(bday_string, self.line_width) + '\n'
        else:
            return ''
    
    def _get_proximity_list(self, today: date) -> List[_Proximity]:
        prox_list = []
        for bday in self._BIRTHDAYS:
            if (bday.date.month == today.month and bday.date.day < today.day
                or bday.date.month < today.month):
                next_bd = date(today.year+1, bday.date.month, bday.date.day)
            else:
                next_bd = date(today.year, bday.date.month, bday.date.day)
            days_until = (next_bd - today).days

            bd_age = None
            if bday.date.year != date.min.year:
                bd_age = next_bd.year - bday.date.year
            
            weekday_desc = None
            weeks_ahead = (
                int(next_bd.strftime('%W')) - int(today.strftime('%W')))
            if weeks_ahead <= 1 and days_until > 1:
                weekday_desc = f' on {self._WEEKDAYS[next_bd.weekday()]}'
                if weeks_ahead == 1 and days_until >= 7:
                    weekday_desc += f' of next week'

            prox_list.append(self._Proximity(days_until, bday.name, bd_age, weekday_desc))
        return prox_list
    
    def _format_proximity_list(self, prox_list) -> str:
        bday_str = ''
        last_i = len(prox_list) - 1
        is_not_first = False
        for i, prox in enumerate(prox_list):
            if prox.days_until > self.birthday_notify_days:
                break
            next_prox_days = None if i == last_i else prox_list[i+1].days_until
            if (is_not_first
                    and prox_list[i-1].days_until == prox.days_until
                    and next_prox_days != prox.days_until):
                bday_str += ' and '
            elif i != 0:
                bday_str += ', '
            bday_str += prox.name
            is_not_first = True
            if prox.bd_age:
                bday_str += f' ({prox.bd_age})'
            if i == last_i or next_prox_days != prox.days_until:
                if prox.weekday_desc:
                    bday_str += prox.weekday_desc
                else:
                    bday_str += self._format_days_until(prox.days_until)
        
        if bday_str == '':
            return None
        else:
            return  f'Birthday of {bday_str}'
    
    def _format_days_until(self, days_until) -> str:
        if days_until == 0:
            return ' today'
        elif days_until == 1:
            return ' tomorrow'
        else:
            return f' in {days_until} days'
