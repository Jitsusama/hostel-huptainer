"""Program bootstrap."""

import os
import sys

from hostel_huptainer.arguments import Arguments
from hostel_huptainer.environment import Environment
from hostel_huptainer.errors import InputError
from hostel_huptainer.output import stdout


def main():
    """Main program logic."""
    try:
        Environment(os.environ)
        Arguments(sys.argv)
    except InputError as error:
        stdout(str(error))
        sys.exit(1)


if __name__ == '__main__':
    main()
