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


def test_returns_error_when_certbot_hostname_is_not_passed():
    try:
        subprocess.check_output(args=['hostel-huptainer'])
    except subprocess.CalledProcessError as exception:
        assert 'CERTBOT_HOSTNAME' in exception.output.decode()
    else:
        pytest.fail('hostel-huptainer did not raise an error.')


def test_prints_usage_when_help_argument_passed():
    stdout = subprocess.check_output(
        args=['hostel-huptainer', '--help'])

    assert 'hostel-huptainer' in stdout.decode()


@pytest.mark.skip('to be tackled later')
def test_restarts_container_with_matching_label(
        python_container):
    python_container.start()

    subprocess.check_call(
        args=['hostel-huptainer'],
        env=os.environ.update({
            'CERTBOT_HOSTNAME': 'testhost.testdomain.tld'}))

    python_container.wait(timeout=2)
    assert 'HUPPED' in python_container.logs()


@pytest.mark.skip('to be tackled later')
def test_does_not_restart_containers_with_mismatched_label(
        python_container):
    python_container.start()

    subprocess.check_call(
        args=['hostel-huptainer'],
        env=os.environ.update({
            'CERTBOT_HOSTNAME': 'idontmatch.testdomain.tld'}))

    python_container.wait(timeout=2)

    assert 'HUPPED' not in python_container.logs()
