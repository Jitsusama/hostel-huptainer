"""Tests the hostel_huptainer.output module."""

import pytest

from hostel_huptainer.system import stderr


@pytest.mark.parametrize('message', ['Help!', 1])
def test_stderr_calls_print_properly_with_truthy_message(mocker, message):
    stub_stderr = mocker.patch('hostel_huptainer.system.sys.stderr')
    mock_print = mocker.patch('hostel_huptainer.system.print')

    stderr(message)

    mock_print.assert_called_once_with(message, file=stub_stderr)


@pytest.mark.parametrize('message', ['', None])
def test_stderr_does_not_call_print_with_falsey_message(mocker, message):
    mock_print = mocker.patch('hostel_huptainer.system.print')

    stderr(message)

    mock_print.assert_not_called()
