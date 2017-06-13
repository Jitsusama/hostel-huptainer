"""Inspects dictionary for desired keys and stores for later usage."""

from hostel_huptainer.errors import InputError


class Environment(object):
    """Searches ``environment`` for expected variables and stores them."""

    def __init__(self, environment):
        self.hostname = environment.get('CERTBOT_HOSTNAME')

        if not self.hostname:
            raise InputError('CERTBOT_HOSTNAME environment variable is missing.')
