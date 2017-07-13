"""Work with Docker containers."""

import docker


def csv_contains_value(csv_list, value):
    """Test whether passed csv list contains passed value."""
    item_list = csv_list.split(',')

    return any([
        item.strip() == value for item in item_list])


class MatchingContainers(object):
    """Iterable for live Docker containers matching filter label value."""

    def __init__(self, label_value):
        self.label_value = label_value
        self.docker = docker.client.DockerClient()

    def __iter__(self):
        """Iterate over each of the matching containers."""
        filters = {'status': 'running',
                   'label':  'org.eff.certbot.cert_cns'}
        containers = self.docker.containers.list(filters=filters)

        for container in containers:
            label_value = container.labels.get('org.eff.certbot.cert_cns')
            if csv_contains_value(label_value, self.label_value):
                yield container
