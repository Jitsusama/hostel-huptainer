"""Tests the hostel_huptainer.__main__ module."""

import pytest
from hostel_huptainer.errors import InputError

from hostel_huptainer.__main__ import main


@pytest.mark.parametrize('environ', [
    {'thing': 'one'}, {'thing': 'two'}])
def test_passes_os_environ_to_environment(mocker, environ):
    mocker.patch('hostel_huptainer.__main__.sys')
    mocker.patch('hostel_huptainer.__main__.InputError')
    stub_environ = mocker.patch(
        'hostel_huptainer.__main__.os.environ',
        value=environ)

    mock_environment = mocker.patch(
        'hostel_huptainer.__main__.Environment')

    main()

    mock_environment.assert_called_once_with(stub_environ)


def test_properly_calls_sys_exit_on_input_error(mocker):
    mocker.patch('hostel_huptainer.__main__.Environment',
                 side_effect=InputError)

    mock_exit = mocker.patch(
        'hostel_huptainer.__main__.sys.exit')

    main()

    mock_exit.assert_called_once_with(1)


@pytest.mark.parametrize('message', ['Danger!', ''])
def test_calls_stdout_with_input_error_message_when_raised(
        mocker, message):
    mocker.patch('hostel_huptainer.__main__.sys')
    mocker.patch('hostel_huptainer.__main__.Environment',
                 side_effect=InputError(message))

    mock_stdout = mocker.patch(
        'hostel_huptainer.__main__.stdout')

    main()

    mock_stdout.assert_called_once_with(message)
