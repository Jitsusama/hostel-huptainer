"""Program bootstrap."""

import os
import sys

from hostel_huptainer.arguments import Arguments
from hostel_huptainer.containers import MatchingContainers, send_signal
from hostel_huptainer.environment import Environment
from hostel_huptainer.errors import InputError, ContainerError
from hostel_huptainer.system import abnormal_exit, error_message


def main():
    """Main program logic."""
    try:
        arguments = Arguments(sys.argv)
        environment = Environment(os.environ)
        containers = MatchingContainers(environment.hostname)
    except InputError as error:
        _handle_error(error)
    except ContainerError as error:
        _handle_error(error)
    else:
        for container in containers:
            send_signal(arguments.signal_method, container)


def _handle_error(error):
    error_message(error)
    abnormal_exit()


if __name__ == '__main__':
    main()
