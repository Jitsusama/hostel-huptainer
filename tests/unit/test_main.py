"""Tests the hostel_huptainer.__main__ module."""

import pytest
from hostel_huptainer.errors import InputError

from hostel_huptainer.__main__ import main


class TestEnvironmentInteractions(object):
    @pytest.mark.parametrize('environ', [
        {'thing': 'one'}, {'thing': 'two'}])
    def test_passes_os_environ_to_environment(self, mocker, environ):
        mocker.patch('hostel_huptainer.__main__.sys')
        mocker.patch('hostel_huptainer.__main__.Arguments')
        mocker.patch('hostel_huptainer.__main__.InputError')
        stub_environ = mocker.patch(
            'hostel_huptainer.__main__.os.environ',
            value=environ)

        mock_environment = mocker.patch(
            'hostel_huptainer.__main__.Environment')

        main()

        mock_environment.assert_called_once_with(stub_environ)

    def test_properly_calls_sys_exit_on_input_error(self, mocker):
        mocker.patch('hostel_huptainer.__main__.Arguments')
        mocker.patch('hostel_huptainer.__main__.Environment',
                     side_effect=InputError)

        mock_exit = mocker.patch(
            'hostel_huptainer.__main__.sys.exit')

        main()

        mock_exit.assert_called_once_with(1)

    @pytest.mark.parametrize('message', ['Danger!', ''])
    def test_calls_stdout_with_input_error_message_when_raised(
            self, mocker, message):
        mocker.patch('hostel_huptainer.__main__.sys')
        mocker.patch('hostel_huptainer.__main__.Arguments')
        mocker.patch('hostel_huptainer.__main__.Environment',
                     side_effect=InputError(message))

        mock_stdout = mocker.patch(
            'hostel_huptainer.__main__.stdout')

        main()

        mock_stdout.assert_called_once_with(message)


class TestArgumentsInteractions(object):
    @pytest.mark.parametrize('argv', [
        ['hostel_huptainer', '--help'],
        ['hostel_huptainer', 'luxembourg']])
    def test_passes_sys_argv_to_arguments(self, mocker, argv):
        mocker.patch('hostel_huptainer.__main__.Environment')
        stub_argv = mocker.patch(
            'hostel_huptainer.__main__.sys.argv',
            value=argv)

        mock_arguments = mocker.patch(
            'hostel_huptainer.__main__.Arguments')

        main()

        mock_arguments.assert_called_once_with(stub_argv)
