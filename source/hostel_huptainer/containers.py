"""Work with Docker containers."""


class MatchingContainers(object):
    """Iterable for live Docker containers matching filter label value."""

    def __init__(self, label_value):
        raise NotImplementedError(label_value)

    def __iter__(self):
        """Iterates over each of the matching containers."""
        raise NotImplementedError()
