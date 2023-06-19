"""
Define `PrimaryPrompt` class.

The method `get_str()` defines the output of the object.

"""

from datetime import datetime, date
from pathlib import Path
from typing import List
import os.path
import shutil
import textwrap

from .birthday_notifier import BirthdayNotifier
from .data_loader import DataLoader
from .exceptions import (
    ConstructTimeTagsGroup, IncorrectParameterTypeError,
    BirthdayNotifyDaysLessThanZeroError, LineWidthLessThanTenError,
    CorruptJSONFileGroup
    )
from .time_tag import TimeTag

sample_json_path = str(Path(__file__).parent / 'sample_time_tag_birthday.json')


class PrimaryPrompt:
    """
    Class for adding time tags to interactive mode primary prompt.

    The object is expected to be assinged to `sys.ps1` to change the
    prompt in interactive mode. This can be done in Python startup
    script. It will also show birthday reminders if day has changed
    (00:00) between two statement entries.
    
    Attributes
    ----------
    birthday_notifier
    default_prompt
    tag_end_prompt
    line_width

    Methods
    -------
    print_birthdays
        Print the list of birthdays.
    print_time_tags
        Print the list of time tags.
    time_machine
        Print birthday notifications from another date.
    """
    
    def __init__(
            self,
            json_path: str = '~/time_tag_birthday.json',
            birthday_notify_days: int = 30,
            default_prompt: str = '>>> ',
            tag_end_prompt: str = '> ',
            line_width: int = 70,
            data_loader: DataLoader | None = None
            ) -> None:
        """
        Initialize a primary prompt object.
        
        Parameters
        ----------
        json_path : str, default '~/time_tag_birthday.json'
            Path to the data file for birthdays and time tags. Strings
            '~' and '~user' are replaced by the user's home directory.
        birthday_notify_days : int, default 30
            How many days before the birthday a notification is shown.
        default_prompt: str, default '>>> '
            Text to be shown in prompt when no time tag is active.
        tag_end_prompt: str, default '> '
            Text to be written in prompt after the time tag.
        line_width : int, default 70
            How many characters fit on one line.
        data_loader : DataLoader or None, default None
            Override `data_loader` for testing purposes.
        
        Raises
        ------
        IncorrectParameterTypeError
            Any of the parameter values have unexpected type.
        BirthdayNotifyDaysLessThanZeroError
            Raised when parameter `birthday_notify_days` is less than 0.
        LineWidthLessThanTenError
            Raised when parameter `line_width` is less than ten.
        OSError
            May be raised if JSON file could not be read or created.
        """
        self.birthday_notifier: BirthdayNotifier
        """Reference to a birthday notifier object if birthday reminders
        should be printed when date changes."""
        self.default_prompt = default_prompt
        """Text to be shown in prompt when no time tag is active."""
        self.tag_end_prompt = tag_end_prompt
        """Text to be written in prompt after the time tag."""
        self.line_width = line_width
        """How many characters fit on one line."""

        self.time_tags: List[TimeTag] | None = None
        self._messages: List[str] = []
        self._last_prompt_date = date.today()
        self._print_init = True
        
        if not (isinstance(data_loader, DataLoader) or data_loader is None):
            raise IncorrectParameterTypeError(
                'data_loader', type(data_loader).__name__, 'primary prompt',
                expected_type='DataLoader or None'
                )
        if data_loader is None:
            if not isinstance(json_path, str):
                raise IncorrectParameterTypeError(
                    'json_path', type(json_path).__name__, 'primary prompt',
                    expected_type='string'
                    )
            json_path = os.path.abspath(os.path.expanduser(json_path))
            try:
                data_loader = self._construct_data_loader(json_path)
            except FileNotFoundError:
                shutil.copy(sample_json_path, json_path)
                self._messages.append(
                    'Created a JSON file with sample data and using it. '
                    f'Creation path: {json_path}'
                    )
                data_loader = self._construct_data_loader(json_path)
        
        self.birthday_notifier = BirthdayNotifier(
            data_loader, birthday_notify_days, line_width)
        
        if not isinstance(birthday_notify_days, int):
            raise IncorrectParameterTypeError(
                'birthday_notify_days', type(birthday_notify_days).__name__,
                'primary prompt', expected_type='integer'
                )
        elif birthday_notify_days < 0:
            raise BirthdayNotifyDaysLessThanZeroError(birthday_notify_days)

        if not isinstance(default_prompt, str):
            raise IncorrectParameterTypeError(
                'default_prompt', type(default_prompt).__name__, 'primary prompt',
                expected_type='string'
                )
        
        if not isinstance(tag_end_prompt, str):
            raise IncorrectParameterTypeError(
                'tag_end_prompt', type(tag_end_prompt).__name__, 'primary prompt',
                expected_type='string'
                )
        
        if not isinstance(line_width, int):
            raise IncorrectParameterTypeError(
                'line_width', type(line_width).__name__, 'primary prompt',
                expected_type='integer'
                )
        elif line_width < 10:
            raise LineWidthLessThanTenError(line_width)

        if data_loader:
            try:
                self.time_tags = data_loader.construct_time_tags()
            except ConstructTimeTagsGroup as err_group:
                self._messages.extend([
                    str(exc) for exc in err_group.exceptions])
        self._messages.extend(self.birthday_notifier.messages)
        
        # Method aliases from BirthdayNotifier
        self.print_birthdays = self.birthday_notifier.print_birthdays
        self.time_machine = self.birthday_notifier.time_machine
    
    def print_time_tags(self) -> None:
        """Print the list of time tags."""
        print()
        if self._print_init or not self.time_tags:
            if self._messages:
                print('\n' + self._format_messages() + '\n')
            else:
                print('\nNo messages.\n')
        self._print_init = False
        if self.time_tags:
            for tag in self.time_tags:
                print(f'{tag.start} to {tag.stop}  {tag.text}{self.tag_end_prompt}')
        print()
    
    def __str__(self) -> str:
        return self.get_str(datetime.now())
    
    def get_str(self, now: datetime):
        prolog = ''
        if self._print_init and self._messages:
            prolog += '\n' + self._format_messages() + '\n'

        today = date(now.year, now.month, now.day)
        if self.birthday_notifier and (
                self._print_init
                or self._last_prompt_date != today):
            prolog += self.birthday_notifier.get_str() + '\n'
        self._last_prompt_date = today

        self._print_init = False
        return prolog + self.get_prompt(now)

    def get_prompt(self, now: datetime) -> str:
        time_tag = self.get_time_tag(now)
        if time_tag:
            return time_tag + self.tag_end_prompt
        else:
            return self.default_prompt
    
    def _format_messages(self) -> str:
        msg_list = []
        for msg in self._messages:
            first_line = textwrap.wrap(msg, self.line_width)[0]
            msg = msg[len(first_line):].lstrip()
            if msg:
                msg = '\n    ' + '\n    '.join(textwrap.wrap(msg, self.line_width-4))
            msg_list.append(first_line + msg)
        return '\n'.join(msg_list)
    
    def get_time_tag(self, now: datetime) -> str | None:
        txt = None
        if self.time_tags:
            for tag in self.time_tags:
                time_start = datetime(
                    now.year, now.month, now.day, *tag.start_tuple)
                time_stop = datetime(
                    now.year, now.month, now.day, *tag.stop_tuple)
                
                if time_start < time_stop:
                    if time_start <= now < time_stop:
                        txt = tag.text
                else:
                    if now >= time_start or now < time_stop:
                        txt = tag.text
        return txt
    
    def _construct_data_loader(self, json_path: str) -> DataLoader | None:
        data_loader = None
        with open(json_path, 'r', encoding='utf-8') as fp:
            try:
                data_loader = DataLoader(fp, json_path)
            except CorruptJSONFileGroup as err_group:
                self._messages.extend(err_group.get_messages())
                return None
        return data_loader
