"""
Define `PrimaryPrompt` class.

The method `__str__()` defines the output of the object.

"""

from datetime import datetime, date
from typing import List

from .daily_prompt import DailyPrompt
from .exceptions import TimeTagErrorGroup, IncorrectReferenceError, format_errors
from .time_tag import TimeTag, get_time_tags


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
    """
    
    def __init__(
            self,
            daily_prompt: DailyPrompt | None = None,
            default_prompt: str = '>>> ',
            tag_end_prompt: str = '> '
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
        """
        self.daily_prompt = daily_prompt
        """Reference to a daily prompt object if birthday reminders
        should be printed when date changes."""
        self.default_prompt: str = default_prompt
        """Text to be shown in prompt when no time tag is active."""
        self.tag_end_prompt: str = tag_end_prompt
        """Text to be written in prompt after the time tag."""

        self._time_tags: List[TimeTag] | None = None
        self._time_tag_error_text: str | None = None
        self._last_prompt_date = date.today()
        
        if not isinstance(daily_prompt, DailyPrompt):
            raise IncorrectReferenceError('daily_prompt', type(daily_prompt))

        try:
            self._time_tags = get_time_tags()
        except TimeTagErrorGroup as err_group:
            self._time_tag_error_text = format_errors(err_group)
            print('\n' + self._time_tag_error_text + '\n')
    
    def print_tags(self) -> None:
        """Print the list of time tags."""
        print()
        if self._time_tag_error_text:
            print(self._time_tag_error_text)
        else:
            for tag in self._time_tags:
                print(f'{tag.start} to {tag.stop}   {tag.text}{self.tag_end_prompt}')
        print()
    
    def __str__(self) -> str:

        if self._time_tag_error_text:
            return self.default_prompt

        prompt = ''

        if self.daily_prompt and self._last_prompt_date != date.today():
            prompt += str(self.daily_prompt) + '\n'
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
