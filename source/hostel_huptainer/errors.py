"""Errors."""


class InputError(Exception):
    """Program input is incorrect."""


class NoMatchesError(Exception):
    """No running containers match hostname."""
