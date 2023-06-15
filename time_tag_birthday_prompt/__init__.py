"""
Add time tags to interactive mode prompt and birthday reminders to
Python startup.

The package introduces three classes to be used while configuring the
prompt. They are intended to be used in a Python startup file.

The list of birthdays for daily prompt can be edited in file
``data_birthdays.py`` and time tags for primary prompt in
``data_time_tags.py``.

Examples
--------
The Python startup file could be written as follows. Note that
initiating `DailyPrompt` will by default print its string form. See
`__init__()` parameter `print_on_init`.

    import sys
    from time_tag_birthday_prompt import (
        DailyPrompt, PrimaryPrompt, SecondaryPrompt)

    daily_prompt = DailyPrompt(birthday_notify_days=30)
    primary_prompt = PrimaryPrompt(daily_prompt)
    secondary_prompt = SecondaryPrompt(primary_prompt)

    sys.ps1 = primary_prompt
    sys.ps2 = secondary_prompt

"""

__version__ = '0.9.0'

from .daily_prompt import DailyPrompt
from .primary_prompt import PrimaryPrompt
from .secondary_prompt import SecondaryPrompt
