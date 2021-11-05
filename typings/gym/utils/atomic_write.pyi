"""
This type stub file was generated by pyright.
"""

import sys
from contextlib import contextmanager

if sys.version_info >= (3, 3): ...
else: ...

@contextmanager
def atomic_write(filepath, binary=..., fsync=...):
    """Writeable file object that atomically updates a file (using a temporary file). In some cases (namely Python < 3.3 on Windows), this could result in an existing file being temporarily unlinked.

    :param filepath: the file path to be opened
    :param binary: whether to open the file in a binary mode instead of textual
    :param fsync: whether to force write the file to disk
    """
    ...
