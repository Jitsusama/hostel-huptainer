"""Tests the hostel_huptainer.__main__ module."""

import pytest
try:
    import unittest.mock as mock
except ImportError:
    import mock
from hostel_huptainer.environment import Environment
from hostel_huptainer.errors import InputError, ContainerError

from hostel_huptainer.__main__ import main


class TestEnvironmentInteractions(object):
    @pytest.mark.parametrize('environ', [
        {'thing': 'one'}, {'thing': 'two'}])
    def test_passes_os_environ_to_environment(self, mocker, environ):
        mocker.patch('hostel_huptainer.__main__.sys')
        mocker.patch('hostel_huptainer.__main__.Arguments')
        mocker.patch('hostel_huptainer.__main__.InputError')
        mocker.patch('hostel_huptainer.__main__.MatchingContainers')
        mocker.patch('hostel_huptainer.__main__.send_signal')
        stub_environ = mocker.patch(
            'hostel_huptainer.__main__.os.environ',
            value=environ)
        mock_environment = mocker.patch(
            'hostel_huptainer.__main__.Environment')

        main()

        mock_environment.assert_called_once_with(stub_environ)

    def test_properly_calls_abnormal_exit_on_input_error(self, mocker):
        mocker.patch('hostel_huptainer.__main__.os')
        mocker.patch('hostel_huptainer.__main__.Arguments')
        mocker.patch('hostel_huptainer.__main__.Environment',
                     side_effect=InputError)
        mocker.patch('hostel_huptainer.__main__.MatchingContainers')
        mocker.patch('hostel_huptainer.__main__.send_signal')
        mock_abnormal_exit = mocker.patch(
            'hostel_huptainer.__main__.abnormal_exit')

        main()

        mock_abnormal_exit.assert_called_once()

    @pytest.mark.parametrize('message', ['Danger!', ''])
    def test_calls_error_message_with_input_error_message_when_raised(
            self, mocker, message):
        stub_error = InputError(message)
        mocker.patch('hostel_huptainer.__main__.os')
        mocker.patch('hostel_huptainer.__main__.sys.argv')
        mocker.patch('hostel_huptainer.__main__.abnormal_exit')
        mocker.patch('hostel_huptainer.__main__.Arguments')
        mocker.patch('hostel_huptainer.__main__.Environment',
                     side_effect=stub_error)
        mocker.patch('hostel_huptainer.__main__.MatchingContainers')
        mocker.patch('hostel_huptainer.__main__.send_signal')
        mock_error_message = mocker.patch(
            'hostel_huptainer.__main__.error_message')

        main()

        mock_error_message.assert_called_once_with(stub_error)


class TestArgumentsInteractions(object):
    @pytest.mark.parametrize('argv', [
        ['hostel_huptainer', '--help'],
        ['hostel_huptainer', 'luxembourg']])
    def test_passes_sys_argv_to_arguments(self, mocker, argv):
        mocker.patch('hostel_huptainer.__main__.os')
        mocker.patch('hostel_huptainer.__main__.Environment')
        mocker.patch('hostel_huptainer.__main__.MatchingContainers')
        mocker.patch('hostel_huptainer.__main__.send_signal')
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
        mocker.patch('hostel_huptainer.__main__.send_signal')
        mock_matches = mocker.patch(
            'hostel_huptainer.__main__.MatchingContainers')

        main()

        mock_matches.assert_called_once_with(hostname)

    def test_properly_calls_abnormal_exit_on_raised_error(self, mocker):
        mocker.patch('hostel_huptainer.__main__.os')
        mocker.patch('hostel_huptainer.__main__.Arguments')
        mocker.patch('hostel_huptainer.__main__.Environment')
        mocker.patch('hostel_huptainer.__main__.MatchingContainers',
                     side_effect=ContainerError)
        mocker.patch('hostel_huptainer.__main__.send_signal')
        mock_abnormal_exit = mocker.patch(
            'hostel_huptainer.__main__.abnormal_exit')

        main()

        mock_abnormal_exit.assert_called_once()

    @pytest.mark.parametrize('message', ['Danger!', ''])
    def test_calls_error_message_with_raised_error_text(
            self, mocker, message):
        stub_error = ContainerError(message)
        mocker.patch('hostel_huptainer.__main__.os')
        mocker.patch('hostel_huptainer.__main__.sys.argv')
        mocker.patch('hostel_huptainer.__main__.abnormal_exit')
        mocker.patch('hostel_huptainer.__main__.Arguments')
        mocker.patch('hostel_huptainer.__main__.Environment')
        mocker.patch('hostel_huptainer.__main__.MatchingContainers',
                     side_effect=stub_error)
        mocker.patch('hostel_huptainer.__main__.send_signal')
        mock_error_message = mocker.patch(
            'hostel_huptainer.__main__.error_message')

        main()

        mock_error_message.assert_called_once_with(stub_error)

    @pytest.mark.parametrize('stub_matches', [
        [mock.MagicMock()],
        [mock.MagicMock(), mock.MagicMock(), mock.MagicMock()]])
    def test_calls_send_signal_on_each_item_of_returned_iterable(
            self, mocker, stub_matches):
        mocker.patch('hostel_huptainer.__main__.os')
        mocker.patch('hostel_huptainer.__main__.sys')
        mocker.patch('hostel_huptainer.__main__.Arguments')
        mocker.patch('hostel_huptainer.__main__.Environment')
        stub_matching = mocker.patch(
            'hostel_huptainer.__main__.MatchingContainers')
        stub_matching.return_value.__iter__ = (
            lambda _: iter(stub_match for stub_match in stub_matches))
        mock_send_signal = mocker.patch(
            'hostel_huptainer.__main__.send_signal')

        main()

        for stub_match in stub_matches:
            mock_send_signal.assert_has_calls([
                mocker.call(mocker.ANY, stub_match)])

    @pytest.mark.parametrize('signal_method', ['reload', 'restart'])
    def test_sends_passed_signal_to_send_signal(
            self, mocker, signal_method):
        mocker.patch('hostel_huptainer.__main__.os')
        mocker.patch('hostel_huptainer.__main__.sys')
        mocker.patch('hostel_huptainer.__main__.Environment')
        stub_arguments = mocker.patch(
            'hostel_huptainer.__main__.Arguments')
        stub_arguments.return_value.signal_method = signal_method
        stub_matching = mocker.patch(
            'hostel_huptainer.__main__.MatchingContainers')
        stub_matching.return_value.__iter__ = (
            lambda _: iter([mocker.MagicMock()]))
        mock_send_signal = mocker.patch(
            'hostel_huptainer.__main__.send_signal')

        main()

        mock_send_signal.assert_has_calls([
            mocker.call(signal_method, mocker.ANY)])
