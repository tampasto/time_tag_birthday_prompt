time_tag_birthday_prompt
========================
Add time tags to interactive mode prompt and birthday reminders to
Python startup.

As every avid coder knows how inexplicably inhumane feat it is to
remember the birthdays of your friends and loved ones, this library
makes it possible to automate the reminders for an arbitrary list of
birthdays. In addition, the library also enables setting up
time-sensitive messages to the prompt text in Python interactive mode
(REPL). For example you may set your prompt to show ``fancy eye bags?>``
from 23:00 to 02:00 and ``zombie‑in‑waiting>`` from 02:00 to 06:00.

As we are only human, the library also abstracts away the Gregorian
notation of birthdays and tells the birthday will be ``on Thursday``
if it is within 6 days and ``on Thursday next week`` if it is in 7
days or more but within next calendar week. More distant birthdays will
be represented as their proximity in days. By default, birthdays within
30 days will be shown.

Example
-------
When the library is correctly set up in the Python startup script,
opening interactive mode with command `py` (Windows) or `python`
(Linux/MacOS) will produce the following output. Note that the example
resembles the output with switch `-q` leaving out Python version and
copyright messages.

```
C:\Users\username>py -q

----------------------------------------------------------------------
Today is Thursday, 2023-06-15
Birthday of Dan Brown (59) on Thursday next week, Martti Ahtisaari
(86) on Friday next week, Elon Musk (52) in 13 days, Aku Louhimies
(55) in 18 days, Jasper Pääkkönen (43) in 30 days
----------------------------------------------------------------------
coffee> _
```

The above example is the output on 15 June 2023 and it's 06:00 to 08:29
o'clock provided the following birthdays and time tags are set in the
JSON file:

```json
{
    "timeTags": [
        ["06:00", "08:30", "coffee"]
    ],
    "birthdays": [
        ["1937-06-23", "Martti Ahtisaari"]
        ,["1964-06-22", "Dan Brown"]
        ,["1968-07-03", "Aku Louhimies"]
        ,["1971-06-28", "Elon Musk"]
        ,["1980-07-15", "Jasper Pääkkönen"]
    ]
}
```

If you do not wish to have time tag prompts or birthday notifications,
you may leave either (or both) of the two JSON keys `null`. Please note
that both keys must always be defined as arrays or nulls in order for
the file to be valid. If `birthdays` key is `null`, the startup prompt
will not be printed.

```json
{
    "timeTags": [
        ["06:00", "08:30", "coffee"]
    ],
    "birthdays": null
}
```

If the tag is still active and user enters a statement, the next prompt
will reprint the tag:

```
coffee> print('Hello, world!')
Hello, world!
coffee> _
```

When the tag is no longer active, the next prompt will show the default
prompt. Here, the prompt is entered at 08:30.

```
coffee> print('Testing')
Testing
>>> _
```

The birthday notifications will be printed when a prompt is entered
after midnight. In the following example, the first statement is entered
at 23:59 on 15 June 2023 and the second at 00:00 on 16 June 2023.

```
>>> print('Today is 15 June.')
Today is 15 June.
>>> print("It's past midnight.")
It's past midnight.

----------------------------------------------------------------------
Today is Friday, 2023-06-16
Birthday of Dan Brown (59) on Thursday, Martti Ahtisaari (86) on
Friday next week, Elon Musk (52) in 12 days, Aku Louhimies (55) in 17
days, Jasper Pääkkönen (43) in 29 days
----------------------------------------------------------------------
>>> _
```

The secondary prompt will follow the indent of the time tags.

```
very long tag> print('Long '
           ... 'statement',
           ... some_variable)
```

The package may also be run as a script. It can be used to check
resolved values for time tags and birthdays. By default, it shows usage.
Replace `py` with `python` in Unix and MacOS.

```
py -m time_tag_birthday_prompt
```

Installing
----------
You may install the package with the following command. Replace `py`
with `python` in Unix and MacOS.

```
py -m pip install time_tag_birthday_prompt@git+https://github.com/tampasto/time_tag_birthday_prompt.git
```

After installing the package it is ready to be imported. However, to set
it up as the default prompt, you must create a startup script. You can
create a new file such as `python_startup.py` in your desired directory
and set the environment variable `PYTHONSTARTUP` to point to this file,
i.e., `path_to_file/python_startup.py`. This file will be run every time
the interactive mode is entered if not purposefully overrided by certain
Python executable isolation switches.

The Python startup file could look like the following:

```python
import sys

from time_tag_birthday_prompt import PrimaryPrompt, SecondaryPrompt

primary_prompt = PrimaryPrompt(
    json_path='~/time_tag_birthday.json',
    birthday_notify_days=30
    )
secondary_prompt = SecondaryPrompt(primary_prompt)

sys.ps1 = primary_prompt
sys.ps2 = secondary_prompt
```

If no file exists in the path defined in parameter `json_path`, a sample
file will be copied there. Strings `~` and `~user` will be replaced by
user directory path, i.e., environment variable USERPROFILE in Windows
and HOME in Unix.

The sample JSON file copied to the `json_path` parameter shows the
format of the file and also contains two non-functional comment keys.
This file is the same file as the one found in the package folder with
name `sample_time_tag_birthday.json`.

Commas are placed in the beginning of the rows as it is more common to
append these lists by copying the last row rather than the second last.
You may edit the file according to your personal preference as long as
it stays valid JSON and holds the general original format.

The edited values in the JSON file will be used when the interactive
prompt is restarted.

To see the full list of parameters of the classes and their
documentation, you may use help function, such as `help(PrimaryPrompt)`.
