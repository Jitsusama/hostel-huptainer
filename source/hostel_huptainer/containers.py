"""Work with Docker containers."""

import docker


class MatchingContainers(object):
    """Iterable for live Docker containers matching filter label value."""

    def __init__(self, label_value):
        self.label_value = label_value
        self.docker = docker.client.DockerClient()

    def __iter__(self):
        """Iterate over each of the matching containers."""
        filters = {'status': 'running',
                   'label':  'org.eff.certbot.cert_cns'}
        self.docker.containers.list(filters=filters)
        yield None
