"""Write data out to console."""

from __future__ import print_function
import sys


def stderr(message):
    """Write message to STDERR, when message is valid."""
    if message:
        print(message, file=sys.stderr)
