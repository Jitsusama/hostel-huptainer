"""Process command line arguments."""

from argparse import ArgumentParser
from hostel_huptainer import __version__


class Arguments(object):
    """Parses command line arguments and acts upon them."""

    def __init__(self, argument_vector):
        description = '''\
SIGHUP docker container processes that have an org.eff.certbot.cert_cns
label value matching the hostname specified in the CERTBOT_HOSTNAME
environment variable.'''
        epilog = '''\
This program requires the CERTBOT_HOSTNAME variable to be present as an
environment variable in order to run. When this is called in connection
with the certbot program, this variable should automatically be set.'''

        parser = ArgumentParser(description=description, epilog=epilog)

        parser.add_argument(
            '-s', '--signal', dest='signal_method', default='reload',
            choices=['reload', 'restart'],
            help=('choose reload (the default) if you want matching '
                  'processes to be SIGHUP\'d, or choose restart if '
                  'you would like matching processes to be stopped '
                  'and then restarted.'))

        parser.add_argument(
            '-v', '--version', action='version', version=__version__)

        parser.parse_args(argument_vector[1:])
