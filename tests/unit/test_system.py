"""Tests the hostel_huptainer.output module."""

import pytest

from hostel_huptainer.system import abnormal_exit, error_message


class TestAbnormalExit(object):
    def test_calls_sys_exit_with_code_one(self, mocker):
        mock_exit = mocker.patch('hostel_huptainer.system.sys.exit')

        abnormal_exit()

        mock_exit.assert_called_once_with(1)


class TestErrorMessage(object):
    def test_calls___str___on_message(self, mocker):
        mocker.patch('hostel_huptainer.system.sys.stderr')
        mocker.patch('hostel_huptainer.system.print')
        mock_message = mocker.MagicMock()

        error_message(mock_message)

        mock_message.__str__.assert_called_once()

    def test_calls_print_properly_with_truthy_message(self, mocker):
        stub_stderr = mocker.patch('hostel_huptainer.system.sys.stderr')
        mock_print = mocker.patch('hostel_huptainer.system.print')

        error_message('stub-message')

        mock_print.assert_called_once_with('stub-message', file=stub_stderr)

    @pytest.mark.parametrize('message', ['', None])
    def test_does_not_call_print_with_falsey_message(
            self, mocker, message):
        mock_print = mocker.patch('hostel_huptainer.system.print')

        error_message(message)

        mock_print.assert_not_called()
