"""Tests the hostel_huptainer.__main__ module."""

import pytest
try:
    import unittest.mock as mock
except ImportError:
    import mock
from hostel_huptainer.environment import Environment
from hostel_huptainer.errors import InputError, NoMatchesError

from hostel_huptainer.__main__ import main


class TestEnvironmentInteractions(object):
    @pytest.mark.parametrize('environ', [
        {'thing': 'one'}, {'thing': 'two'}])
    def test_passes_os_environ_to_environment(self, mocker, environ):
        mocker.patch('hostel_huptainer.__main__.sys')
        mocker.patch('hostel_huptainer.__main__.Arguments')
        mocker.patch('hostel_huptainer.__main__.InputError')
        mocker.patch('hostel_huptainer.__main__.MatchingContainers')
        stub_environ = mocker.patch(
            'hostel_huptainer.__main__.os.environ',
            value=environ)
        mock_environment = mocker.patch(
            'hostel_huptainer.__main__.Environment')

        main()

        mock_environment.assert_called_once_with(stub_environ)

    def test_properly_calls_sys_exit_on_input_error(self, mocker):
        mocker.patch('hostel_huptainer.__main__.os')
        mocker.patch('hostel_huptainer.__main__.Arguments')
        mocker.patch('hostel_huptainer.__main__.Environment',
                     side_effect=InputError)
        mocker.patch('hostel_huptainer.__main__.MatchingContainers')
        mock_exit = mocker.patch('hostel_huptainer.__main__.sys.exit')

        main()

        mock_exit.assert_called_once_with(1)

    @pytest.mark.parametrize('message', ['Danger!', ''])
    def test_calls_stderr_with_input_error_message_when_raised(
            self, mocker, message):
        mocker.patch('hostel_huptainer.__main__.os')
        mocker.patch('hostel_huptainer.__main__.sys')
        mocker.patch('hostel_huptainer.__main__.Arguments')
        mocker.patch('hostel_huptainer.__main__.Environment',
                     side_effect=InputError(message))
        mocker.patch('hostel_huptainer.__main__.MatchingContainers')
        mock_stderr = mocker.patch('hostel_huptainer.__main__.stderr')

        main()

        mock_stderr.assert_called_once_with(message)


class TestArgumentsInteractions(object):
    @pytest.mark.parametrize('argv', [
        ['hostel_huptainer', '--help'],
        ['hostel_huptainer', 'luxembourg']])
    def test_passes_sys_argv_to_arguments(self, mocker, argv):
        mocker.patch('hostel_huptainer.__main__.os')
        mocker.patch('hostel_huptainer.__main__.Environment')
        mocker.patch('hostel_huptainer.__main__.MatchingContainers')
        stub_argv = mocker.patch(
            'hostel_huptainer.__main__.sys.argv',
            value=argv)
        mock_arguments = mocker.patch(
            'hostel_huptainer.__main__.Arguments')

        main()

        mock_arguments.assert_called_once_with(stub_argv)


class TestMatchingContainersInteractions(object):
    @pytest.mark.parametrize('hostname', ['a.com', 'b.com'])
    def test_passes_hostname(self, mocker, hostname):
        mocker.patch('hostel_huptainer.__main__.os')
        mocker.patch('hostel_huptainer.__main__.sys')
        mocker.patch('hostel_huptainer.__main__.Arguments')
        mocker.patch('hostel_huptainer.__main__.Environment',
                     spec=Environment, hostname=hostname)
        mock_matches = mocker.patch(
            'hostel_huptainer.__main__.MatchingContainers')

        main()

        mock_matches.assert_called_once_with(hostname)

    def test_properly_calls_sys_exit_on_raised_error(self, mocker):
        mocker.patch('hostel_huptainer.__main__.os')
        mocker.patch('hostel_huptainer.__main__.Arguments')
        mocker.patch('hostel_huptainer.__main__.Environment')
        mocker.patch('hostel_huptainer.__main__.MatchingContainers',
                     side_effect=NoMatchesError)
        mock_exit = mocker.patch('hostel_huptainer.__main__.sys.exit')

        main()

        mock_exit.assert_called_once_with(1)

    @pytest.mark.parametrize('message', ['Danger!', ''])
    def test_calls_stderr_with_raised_error_text(self, mocker, message):
        mocker.patch('hostel_huptainer.__main__.os')
        mocker.patch('hostel_huptainer.__main__.sys')
        mocker.patch('hostel_huptainer.__main__.Arguments')
        mocker.patch('hostel_huptainer.__main__.Environment')
        mocker.patch('hostel_huptainer.__main__.MatchingContainers',
                     side_effect=NoMatchesError(message))
        mock_stderr = mocker.patch('hostel_huptainer.__main__.stderr')

        main()

        mock_stderr.assert_called_once_with(message)

    @pytest.mark.parametrize('stub_matches', [
        [mock.MagicMock()],
        [mock.MagicMock(), mock.MagicMock(), mock.MagicMock()]])
    def test_calls_sighup_on_each_item_of_returned_iterable(
            self, mocker, stub_matches):
        mocker.patch('hostel_huptainer.__main__.os')
        mocker.patch('hostel_huptainer.__main__.sys')
        mocker.patch('hostel_huptainer.__main__.Arguments')
        mocker.patch('hostel_huptainer.__main__.Environment')

        stub_matching = mocker.patch(
            'hostel_huptainer.__main__.MatchingContainers')
        stub_matching.return_value.__iter__ = (
            lambda _: iter(stub_match for stub_match in stub_matches))

        main()

        for mock_match in stub_matches:
            mock_match.assert_has_calls([mocker.call.sighup()])
