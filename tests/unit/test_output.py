"""Tests the hostel_huptainer.output module."""

import pytest

from hostel_huptainer.output import stdout


@pytest.mark.parametrize('message', ['Help!', 1])
def test_stdout_calls_print_properly_with_truthy_message(mocker, message):
    mock_print = mocker.patch(
        'hostel_huptainer.output.print')

    stdout(message)

    mock_print.assert_called_once_with(message)


@pytest.mark.parametrize('message', ['', None])
def test_stdout_does_not_call_print_with_falsey_message(mocker, message):
    mock_print = mocker.patch(
        'hostel_huptainer.output.print')

    stdout(message)

    mock_print.assert_not_called()
