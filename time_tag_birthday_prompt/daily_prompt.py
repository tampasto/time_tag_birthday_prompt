"""
Define `DailyPrompt` class for birthday notifications.

"""

from datetime import datetime, date
from typing import List
import collections
import textwrap

from .birthday import Birthday
from .data_loader import DataLoader
from .exceptions import ConstructBirthdaysGroup


class DailyPrompt:
    """
    Class for printing weekdays and birthday reminders on interactive
    mode startup.
    
    Attributes
    ----------
    birthday_notify_days
        How many days before the birthday a notification is shown. Copy
        of PrimaryPrompt value.
    line_width
        How many characters fit on one line. Copy of PrimaryPrompt
        value.
    birthdays
        List of  `Birthday` objects.
    """
    _BDTuple = collections.namedtuple('_BDTuple', ['date', 'name'])
    _Proximity = collections.namedtuple('_Proximity', [
        'days_until', 'name', 'bd_age', 'weekday_desc'])
    _WEEKDAYS = [
        'Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday', 'Saturday',
        'Sunday'
        ]

    def __init__(
            self, data_loader: DataLoader | None, birthday_notify_days: int,
            line_width: int
            ) -> None:
        """
        Initialize a daily prompt object. Invoked by PrimaryPrompt.
        
        Parameters
        ----------
        data_loader : DataLoader or None
            An instance of DataLoader object.
        birthday_notify_days : int
            How many days before the birthday a notification is shown.
        line_width : int
            How many characters fit on one line.
        """
        self.birthday_notify_days = birthday_notify_days
        """How many days before the birthday a notification is shown."""
        self.line_width = line_width
        """How many characters fit on one line."""
        self.birthdays: List[Birthday] | None = None
        """List of `Birthday` objects."""

        self._messages: List[str] = []
        self._print_init = True
        self._birthdays_disabled = False

        if data_loader:
            self._birthdays_disabled = data_loader.birthdays_disabled
            try:
                self.birthdays = data_loader.construct_birthdays()
            except ConstructBirthdaysGroup as err_group:
                self._messages.extend([
                    str(err) for err in err_group.exceptions])
    
    def time_machine(self, date_string: str) -> None:
        """
        Print birthday notifications from another date.
        
        Parameters
        ----------
        date_string : str
            Destination time in format YYYY-MM-DD.
        """
        dt = datetime.strptime(date_string, '%Y-%m-%d')
        d = date(dt.year, dt.month, dt.day)
        print(self.get_str(today=d))
        
    def print_birthdays(self) -> None:
        """Print the list of birthdays."""
        print()
        if self._print_init or not self.birthdays:
            if self._messages:
                print('\n' + self._format_messages() + '\n')
            else:
                print('No birthdays or messages.')
        self._print_init = False
        if self.birthdays:
            for bday in self.birthdays:
                date_str = None
                if isinstance(bday.date, date):
                    date_str = bday.date.strftime('%Y-%m-%d')
                else:
                    date_str = bday.date
                print(f'{date_str}  {bday.name}')
        print()
    
    def __str__(self) -> str:
        return self.get_str()
    
    def get_str(
            self, today: date | None = None
            ) -> str:
        if self._birthdays_disabled:
            return ''
        if today is None:
            today = date.today()
        ret_str = ''
        if self._print_init and self._messages:
            ret_str += '\n' + self._format_messages() + '\n'
        self._print_init = False
        ret_str += (
            '\n' + self.line_width * '-' + '\n'
            + self._format_date(today) + '\n'
            )
        if self.birthdays:
            ret_str += self._format_birthdays(today) + '\n'
        ret_str += self.line_width * '-'
        return ret_str
    
    def _format_messages(self) -> str:
        msg_list = []
        for msg in self._messages:
            first_line = textwrap.wrap(msg, self.line_width)[0]
            msg = msg[len(first_line):].lstrip()
            if msg:
                msg = '\n    ' + '\n    '.join(textwrap.wrap(msg, self.line_width-4))
            msg_list.append(first_line + msg)
        return '\n'.join(msg_list)
    
    def _format_date(self, today: date) -> str:
        d_str = datetime(today.year, today.month, today.day).strftime(
            '%A, %Y-%m-%d')
        return textwrap.fill(f'Today is {d_str}\n', self.line_width)
    
    def _format_birthdays(self, today: date) -> str:
        prox_list = self._get_proximity_list(today)
        prox_list.sort()
        bday_string = self._format_proximity_list(prox_list)
        if bday_string is not None:
            return textwrap.fill(bday_string, self.line_width)
        else:
            return ''
    
    def _get_proximity_list(self, today: date) -> List[_Proximity]:
        prox_list = []
        for bday in self.birthdays:
            if (bday.date_obj.month == today.month and bday.date_obj.day < today.day
                or bday.date_obj.month < today.month):
                next_bd = date(today.year+1, bday.date_obj.month, bday.date_obj.day)
            else:
                next_bd = date(today.year, bday.date_obj.month, bday.date_obj.day)
            days_until = (next_bd - today).days

            bd_age = None
            if bday.date_obj.year != date.min.year:
                bd_age = next_bd.year - bday.date_obj.year
            
            weekday_desc = None
            weeks_ahead = (
                int(next_bd.strftime('%W')) - int(today.strftime('%W')))
            if weeks_ahead <= 1 and days_until > 1:
                weekday_desc = f' on {self._WEEKDAYS[next_bd.weekday()]}'
                if weeks_ahead == 1 and days_until >= 7:
                    weekday_desc += f' next week'

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

            if prox.name.strip():
                bday_str += prox.name
            else:
                bday_str += '<empty>'

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
