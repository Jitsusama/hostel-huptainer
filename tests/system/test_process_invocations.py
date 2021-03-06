"""Test basic functionality of the program, end-to-end."""

import os
import subprocess
import pytest
import requests
from hostel_huptainer import __version__

# ATTENTION: See conftest.py for py.test fixtures.


def test_returns_error_when_certbot_hostname_is_not_passed():
    try:
        subprocess.check_output(
            args=['hostel-huptainer'],
            stdin=None, stderr=subprocess.STDOUT)
    except subprocess.CalledProcessError as exception:
        assert 'CERTBOT_HOSTNAME' in exception.output.decode()
    else:
        pytest.fail('hostel-huptainer did not raise an error.')


def test_prints_usage_when_help_argument_passed():
    stdout = subprocess.check_output(
        args=['hostel-huptainer', '--help'])

    assert 'hostel-huptainer' in stdout.decode()


def test_prints_version_when_version_argument_passed():
    # py2.7 sends version to stderr instead of stdout, so we're
    # redirecting stderr to stdout to allow this test to pass.
    stdout = subprocess.check_output(
        args=['hostel-huptainer', '--version'],
        stderr=subprocess.STDOUT)

    assert __version__ in stdout.decode()


def test_reloads_container_with_matching_label(
        python_container):
    python_container.start()

    subprocess.check_call(
        args=['hostel-huptainer'],
        env=os.environ.update({
            'CERTBOT_HOSTNAME': 'testhost.testdomain.tld'}))

    python_container.wait(timeout=2)
    assert 'HUPPED' in python_container.logs().decode()


def test_does_not_reload_containers_with_mismatched_label(
        python_container):
    python_container.start()

    subprocess.check_call(
        args=['hostel-huptainer'],
        env=os.environ.update({
            'CERTBOT_HOSTNAME': 'idontmatch.testdomain.tld'}))

    try:
        python_container.wait(timeout=6)
    except requests.ReadTimeout:
        assert 'HUPPED' not in python_container.logs().decode()


def test_reloads_container_with_matching_label_when_asked(
        python_container):
    python_container.start()

    subprocess.check_call(
        args=['hostel-huptainer', '--signal', 'reload'],
        env=os.environ.update({
            'CERTBOT_HOSTNAME': 'testhost.testdomain.tld'}))

    python_container.wait(timeout=2)
    assert 'HUPPED' in python_container.logs().decode()


def test_restarts_container_with_matching_label_when_asked(
        python_container):
    python_container.start()

    subprocess.check_call(
        args=['hostel-huptainer', '--signal', 'restart'],
        env=os.environ.update({
            'CERTBOT_HOSTNAME': 'testhost.testdomain.tld'}))

    try:
        python_container.wait(timeout=6)
    except requests.ReadTimeout:
        assert 'TERMED' in python_container.logs().decode()
