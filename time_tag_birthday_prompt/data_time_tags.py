"""
Definitions of time tags.

`TIME_TAGS` is a list of 3-tuples. The tuple items are:
    1. Start time
    2. Stop time
    3. Tag name

The tag will be active on the minute of start time and on all the
minutes between start and stop time. It will not be active on the minute
of stop time. In other words, it works like Python slice notation
`minutes[start:stop]`.

Start time must come before stop time except if the stop time is
'00:00'.

It is recommended to use tags of at least 2 characters when using
default prompts to keep indentation coherent. If not using defaults, the
recommended minimum length is:

>>> len(secondary_prompt.prompt) - len(primary_prompt.tag_end_prompt)

"""

from typing import List, Tuple


TIME_TAGS: List[Tuple[str, str, str]] = [
    ('00:00', '02:00', 'fancy eye bags?'),
    ('02:00', '06:00', 'zombie-in-waiting'),
    ('06:00', '08:30', 'coffee time'),
    ('10:50', '11:50', 'lunch'),
    ('22:00', '00:00', 'getting late'),
    ]
