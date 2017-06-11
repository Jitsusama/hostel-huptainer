"""Program bootstrap."""

import os

from hostel_huptainer.environment import Environment


def main():
    Environment(os.environ)


if __name__ == '__main__':
    main()
