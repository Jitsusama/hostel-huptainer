"""Errors."""


class InputError(Exception):
    """Program input is incorrect."""


class ContainerError(Exception):
    """Error encountered while communicating with container daemon."""
