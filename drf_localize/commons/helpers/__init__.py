import os
from contextlib import suppress


# Create your helper functions here.

def format_lazy(s, *args, **kwargs):
    return s.format(*args, **kwargs)


def upsert_file(path):
    """
    Create sub-folders and folders by path
    """

    # Ignore exception if setting a file without a directory
    with suppress(FileNotFoundError):
        os.makedirs(os.path.dirname(path), exist_ok=True)
