"""Testing utils."""

import os
import contextlib


def iterable_mock_open(read_data):
    """Version of `mock.mock_open` that supports iteration
    (required when mocking `open` for `configparser.read`).

    Note the difference:

        1) iteration not working with `mock.mock_open`:

            >>> with mock.patch('builtins.open', mock.mock_open('1\n2\n3'), create=True):
            ...  for x in open('asd'):
            ...   print(x)
            ...
            Traceback (most recent call last):
            File "<stdin>", line 1, in <module>
            File "/usr/lib/python3.5/unittest/mock.py", line 2361, in mock_open
                mock.side_effect = reset_data
            AttributeError: 'str' object has no attribute 'side_effect'

        2) iteration working with our `iterable_mock_open`

            >>> with mock.patch('builtins.open', iterable_mock_open('1\n2\n3'), create=True):
            ...  for x in open('asd'):
            ...   print(x)
            ...
            1
            2
            3
    """
    # python version specific
    raise NotImplementedError


# py2/3 mock support
try:
    # python 3
    from unittest import mock

    def iterable_mock_open(read_data):
        m = mock.mock_open(read_data=read_data)
        m.return_value.__iter__ = lambda self: self
        m.return_value.__next__ = lambda self: next(iter(self.readline, ''))
        return m

    configparser_open_namespace = "configparser.open"

except ImportError:  # pragma: no cover
    # python 2
    import mock

    def iterable_mock_open(read_data):
        m = mock.mock_open(read_data=read_data)
        m.return_value.__iter__ = lambda self: iter(self.readline, '')
        return m

    configparser_open_namespace = "backports.configparser.open"


@contextlib.contextmanager
def isolated_environ(add=None, remove=None, remove_dwave=False, empty=False):
    """Context manager for modified process environment isolation.

    Environment variables can be updated, added and removed. Complete
    environment can be cleared, or cleared only only of a subset of variables
    that affect config loading (``DWAVE_*`` and ``DW_INTERNAL__*`` vars).

    On context clear, original `os.environ` is restored.

    Args:
        add (dict/Mapping):
            Values to add (or update) to the isolated `os.environ`.

        remove (dict/Mapping, or set/Iterable):
            Values to remove from the isolated `os.environ`.

        remove_dwave (bool, default=False):
            Remove dwave-cloud-client specific variables that affect config
            loading (prefixed with ``DWAVE_`` or ``DW_INTERNAL__``)

        empty (bool, default=False):
            Return empty environment.

    Context:
        Modified copy of global `os.environ`. Restored on context exit.
    """

    if add is None:
        add = {}

    with mock.patch.dict(os.environ, values=add, clear=empty):
        for key in frozenset(os.environ.keys()):
            if remove and key in remove:
                os.environ.pop(key, None)
            if remove_dwave and (key.startswith("DWAVE_") or key.startswith("DW_INTERNAL__")):
                os.environ.pop(key, None)

        yield os.environ
