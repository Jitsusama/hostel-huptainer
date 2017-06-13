"""py.test fixtures commonly used by system tests."""

import docker
import pytest

PYTHON_HUPPABLE_CMD_ARGS = ['python2', '-c', '''
import signal
def h(*args): raise Exception('HUPPED')
signal.signal(signal.SIGHUP, h)
while True: pass''']


@pytest.fixture
def python_container():
    client = docker.client.DockerClient()
    image = client.images.get('python:2.7')
    container = client.containers.create(
        image=image, command=PYTHON_HUPPABLE_CMD_ARGS,
        labels={'org.eff.certbot.cert_cns': 'testhost.testdomain.tld'})

    yield container

    container.stop(timeout=1)
    container.remove()
