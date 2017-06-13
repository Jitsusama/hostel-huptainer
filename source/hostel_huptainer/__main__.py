"""Program bootstrap."""

import os
import sys

from hostel_huptainer.arguments import Arguments
from hostel_huptainer.environment import Environment
from hostel_huptainer.errors import InputError
from hostel_huptainer.output import stderr


def main():
    """Main program logic."""
    Arguments(sys.argv)
    try:
        Environment(os.environ)
    except InputError as error:
        stderr(str(error))
        sys.exit(1)


if __name__ == '__main__':
    main()
