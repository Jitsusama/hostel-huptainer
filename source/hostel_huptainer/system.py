"""Write data out to console."""

from __future__ import print_function
import sys


def abnormal_exit():
    """Exits program under abnormal conditions."""
    sys.exit(1)


def error_message(message):
    """Write message to STDERR, when message is valid."""
    if message:
        print(message, file=sys.stderr)
