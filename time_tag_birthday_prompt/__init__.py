"""
Add time tags to interactive mode prompt and birthday reminders to
Python startup.

The package introduces two classes to be used while configuring the
prompt. They are intended to be used in a Python startup file.

The lists of birthdays and time tags are found from a JSON data file
whose location is specified in the parameter `json_path` of
`PrimaryPrompt`. If the file does not exist when primary prompt is
created, a sample file will be copied to this location.

Examples
--------
The Python startup file could be written as follows. See `__init__()`
parameter `print_on_init`.

    import sys
    from time_tag_birthday_prompt import PrimaryPrompt, SecondaryPrompt

    primary_prompt = PrimaryPrompt(birthday_notify_days=30)
    secondary_prompt = SecondaryPrompt(primary_prompt)

    sys.ps1 = primary_prompt
    sys.ps2 = secondary_prompt

"""

package_name = 'time_tag_birthday_prompt'
__version__ = '1.0.0'

from .primary_prompt import PrimaryPrompt
from .secondary_prompt import SecondaryPrompt

from .exceptions import (
    IncorrectParameterTypeError, LineWidthLessThanTenError,
    BirthdayNotifyDaysLessThanZeroError
    )
