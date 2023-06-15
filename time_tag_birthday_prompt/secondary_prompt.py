"""
Define `SecondaryPrompt` class.

The method `__str__()` defines the output of the object.

"""

from datetime import datetime

from .exceptions import IncorrectParameterTypeError
from .primary_prompt import PrimaryPrompt


class SecondaryPrompt:
    """
    Class for following primary prompt indentation in interactive mode.

    The object is expected to be assinged to `sys.ps2` to change the
    prompt in interactive mode. This can be done in Python startup
    script.
    
    Attributes
    ----------
    daily_prompt
    prompt
    """
    
    def __init__(self, primary_prompt: PrimaryPrompt, prompt: str = '... '):
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
            raise IncorrectParameterTypeError(
                'primary_prompt', type(primary_prompt).__name__,
                'secondary prompt', expected_type='PrimaryPrompt object'
                )
        if not isinstance(prompt, str):
            raise IncorrectParameterTypeError(
                'prompt', type(primary_prompt).__name__, 'secondary prompt',
                expected_type='string'
                )

    def __str__(self):
        return self.get_str(datetime.now())
    
    def get_str(self, now: datetime):
        time_tag = self._primary_prompt.get_time_tag(now)
        primary_len = None
        if time_tag is None:
            primary_len = len(self._primary_prompt.default_prompt)
        else:
            primary_len = len(time_tag + self._primary_prompt.tag_end_prompt)
        
        return f'{self.prompt:>{primary_len}}'
