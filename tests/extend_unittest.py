from collections import Counter
from typing import List
from unittest import TestCase


def assertGroupMatchesExceptions(
        self: TestCase, exc_group: ExceptionGroup, type_list: List):
    """
    Fail if exception types in `exc_group` do not match `type_list`.
    """
    expected_counts = Counter(type_list)
    got_counts = Counter([type(err) for err in exc_group.exceptions])
    fail_strings = []
    for err, expected_count in expected_counts.items():
        prolog = f'{err.__name__}: {expected_count} expected, got '
        if err in got_counts:
            if got_counts[err] != expected_count:
                fail_strings.append(prolog + str(got_counts[err]))
        else:
            fail_strings.append(prolog + 'none')
    if len(fail_strings) > 0:
        self.fail(exc_group.__class__.__name__ + '[] -> ' + ', '.join(fail_strings))


class OverridePrint:
    """Callable class to override `print()`.
    
    Only takes an optional single string argument.
    """

    def __init__(self):
        self.text = ''

    def __call__(self, print_string: str | None = None) -> None:
        """Append string `OverridePrint.text`."""
        if print_string is not None:
            self.text += print_string
        self.text += '\n'
