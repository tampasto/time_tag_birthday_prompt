"""
Define `PrimaryPrompt` class.

The method `__str__()` defines the output of the object.

"""

from datetime import datetime, date
from typing import List
import textwrap

from .daily_prompt import DailyPrompt
from .exceptions import TimeTagErrorGroup, IncorrectReferenceError
from .time_tag import TimeTag, construct_time_tags
import data_time_tags


class PrimaryPrompt:
    """
    Class for adding time tags to REPL primary prompt.

    The object is expected to be assinged to `sys.ps1` to change the
    prompt in REPL. This can be done in Python startup script. It will
    also show birthday reminders if day has changed (00:00) between two
    REPL statement entries.
    
    Attributes
    ----------
    daily_prompt
    default_prompt
    tag_end_prompt
    line_width
    daily_prompt_on_init
    """
    
    def __init__(
            self,
            daily_prompt: DailyPrompt | None = None,
            default_prompt: str = '>>> ',
            tag_end_prompt: str = '> ',
            line_width: int = 70,
            daily_prompt_on_init: bool = True
            ) -> None:
        """Initialize a primary prompt object.
        
        Parameters
        ----------
        daily_prompt: DailyPrompt or None, default None
            Reference to a daily prompt object if birthday reminders
            should be printed when date changes.
        default_prompt: str, default '>>> '
            Text to be shown in prompt when no time tag is active.
        tag_end_prompt: str, default '> '
            Text to be written in prompt after the time tag.
        line_width : int, default 70
            How many characters fit on one line.
        daily_prompt_on_init : bool, default True
            If True, print the daily prompt on initialization.
        """
        self.daily_prompt = daily_prompt
        """Reference to a daily prompt object if birthday reminders
        should be printed when date changes."""
        self.default_prompt = default_prompt
        """Text to be shown in prompt when no time tag is active."""
        self.tag_end_prompt = tag_end_prompt
        """Text to be written in prompt after the time tag."""
        self.line_width = line_width
        """How many characters fit on one line."""
        self.print_daily_prompt = daily_prompt_on_init
        """If True, prepend daily prompt text to next primary prompt."""

        self._time_tags: List[TimeTag] | None = None
        self._time_tag_errors: List[str] = []
        self._last_prompt_date = date.today()
        self._print_errors = False
        
        if not isinstance(daily_prompt, DailyPrompt) and daily_prompt is not None:
            raise IncorrectReferenceError('daily_prompt', type(daily_prompt))

        try:
            self._time_tags = construct_time_tags(data_time_tags.TIME_TAGS)
        except TimeTagErrorGroup as err_group:
            self._time_tag_errors = [
                textwrap.fill(str(exc)) for exc in err_group.exceptions]
            self._print_errors = True
    
    def print_tags(self) -> None:
        """Print the list of time tags."""
        print()
        if self._time_tag_errors:
            print('\n'.join(self._time_tag_errors))
        else:
            for tag in self._time_tags:
                print(f'{tag.start} to {tag.stop}   {tag.text}{self.tag_end_prompt}')
        print()
    
    def __str__(self) -> str:
        prompt = ''
        if self._print_errors:
            prompt += '\n' + '\n'.join(self._time_tag_errors) + '\n'
            self._print_errors = False
        if self._time_tag_errors:
            return prompt + self.default_prompt

        if self.daily_prompt and (
                self.print_daily_prompt
                or self._last_prompt_date != date.today()):
            prompt += self.daily_prompt.get_str(self.line_width) + '\n'
            self.print_daily_prompt = False
        self._last_prompt_date = date.today()

        time_tag = self._get_time_tag(datetime.now())

        if time_tag:
            prompt += time_tag + self.tag_end_prompt
        else:
            prompt += self.default_prompt
        return prompt
    
    def _get_time_tag(self, now: datetime) -> str | None:
        for tag in self._time_tags:
            time_start = datetime(
                now.year, now.month, now.day, *tag.start_tuple)
            day_adjust_stop = 1 if tag.stop == (0, 0) else 0
            time_stop = datetime(
                now.year, now.month, now.day+day_adjust_stop, *tag.stop_tuple)

            if time_start <= now < time_stop:
                return tag.text
        return None
