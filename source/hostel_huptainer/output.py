"""Write data out to console."""

from __future__ import print_function


def stdout(message):
    """Write message to STDOUT, when message is valid."""
    if message:
        print(message)
