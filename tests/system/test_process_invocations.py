"""Test basic functionality of the program, end-to-end."""

import os
import subprocess

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


def test_restarts_container_with_matching_label(
        python_container):
    python_container.start()

    subprocess.check_call(
        args=['hostel-huptainer'],
        env=os.environ.update({
            'CERTBOT_HOSTNAME': 'testhost.testdomain.tld'}))

    python_container.wait(timeout=2)
    assert 'HUPPED' in python_container.logs()
