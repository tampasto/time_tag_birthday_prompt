time_tag_birthday_prompt
========================
Add time tags to interactive mode prompt and birthday reminders to
Python startup.

As every avid coder knows how inexplicably inhumane feat it is to
remember the birthdays of your friends and loved ones, this library
makes it possible to automate the reminders for an arbitrary list of
birthdays. No more waking up to a grumpy face and silent treatment when
you were 'simply' supposed to buy a box of chocolates the day before. In
addition, the library also enables setting up time-sensitive messages to
the prompt text in Python interactive mode (REPL). For example you may
set your prompt to show ``fancy eye bags?>`` from 00:00 to 02:00 and
``zombie-in-waiting>`` from 02:00 to 06:00.

As we are only human, the library also abstracts away the Gregorian
notation of birthdays and tells the birthday will be ``on Thursday``
if it is within 6 days and ``on Thursday next week`` if it is in 7
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
coffee time> _
```

The above example is the output on 15 June 2023 and it's 06:00 to 08:29
o'clock providing the following default values:

```
BIRTHDAYS = [
    ('1937-06-23', 'Martti Ahtisaari'),
    ('1964-06-22', 'Dan Brown'),
    ('1968-07-03', 'Aku Louhimies'),
    ('1971-06-28', 'Elon Musk'),
    ('1980-07-15', 'Jasper Pääkkönen'),
    ]
TIME_TAGS = [
    ('06:00', '08:30', 'coffee time'),
    ]
```

If the tag is still active and user enters a statement, the next prompt
will reprint the tag:

```
coffee time> print('Hello, world!')
Hello, world!
coffee time> _
```

When the tag is no longer active, the next prompt will show the default
prompt. Here, the prompt is entered at 08:30.

```
coffee time> print('Testing')
Testing
>>> _
```

If the reference of `DailyPrompt` object has been handed as a parameter
to the initialization of `PrimaryPrompt` object, the birthdays will be
printed when a prompt is entered after midnight. In the following
example, the first statement is entered at 23:59 on 15 June 2023 and the
second at 00:00 on 16 June 2023.

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
coffee time> print('Long '
         ... 'statement',
         ... some_variable)
```
