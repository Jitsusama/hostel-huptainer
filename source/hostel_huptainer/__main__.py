"""Program bootstrap."""

import os
import sys

from hostel_huptainer.environment import Environment
from hostel_huptainer.errors import InputError


def main():
    """Main program logic."""
    try:
        Environment(os.environ)
    except InputError:
        sys.exit(1)


if __name__ == '__main__':
    main()
