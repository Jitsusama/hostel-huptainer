"""Process command line arguments."""

from argparse import ArgumentParser


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
        parser.parse_args(argument_vector[1:])