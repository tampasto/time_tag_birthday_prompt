"""
Define `SecondaryPrompt` class.

The method `__str__()` defines the output of the object.

"""

from datetime import datetime

from .exceptions import IncorrectReferenceError
from .primary_prompt import PrimaryPrompt


class SecondaryPrompt:
    """
    Class for following REPL primary prompt indentation.

    The object is expected to be assinged to `sys.ps2` to change the
    prompt in REPL. This can be done in Python startup script.
    
    Attributes
    ----------
    daily_prompt
    prompt
    """
    
    def __init__(self, primary_prompt: PrimaryPrompt, prompt: str | None = '... '):
        """Initialize a secondary prompt object.
        
        Parameters
        ----------
        primary_prompt : PrimaryPrompt
            Reference to a primary prompt object.
        prompt : str or None, default '... '
            Text in secondary prompt.
        """
        self.prompt = prompt
        """Text in secondary prompt."""

        self._primary_prompt = primary_prompt
        
        if not isinstance(primary_prompt, PrimaryPrompt):
            raise IncorrectReferenceError('primary_prompt', type(primary_prompt))

    def __str__(self):
        time_tag = self._primary_prompt._get_time_tag(datetime.now())
        tag_end_len = len(self._primary_prompt.tag_end_prompt)
        if time_tag is None or len(time_tag) <= len(self.prompt)-tag_end_len:
            return self.prompt
        else:
            indent = len(time_tag) + tag_end_len - 4
            return (indent * ' ') + '... '
