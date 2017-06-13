"""Tests the hostel_huptainer.arguments module."""

import pytest

from hostel_huptainer.arguments import Arguments


def test_passes_usage_information_to_argumentparser(mocker):
    mock_parser = mocker.patch('hostel_huptainer.arguments.ArgumentParser')

    Arguments([])

    mock_parser.assert_called_once_with(
        description=mocker.ANY, epilog=mocker.ANY)


@pytest.mark.parametrize('stub_argv, expected_args', [
    (['hostel-huptainer', '-a', '-b'], ['-a', '-b']),
    (['hostel-huptainer', '--help'], ['--help']),
    (['hostel-huptainer'], []),
])
def test_passes_arguments_and_not_progname_to_parse_args(
        mocker, stub_argv, expected_args):
    mock_parser = mocker.patch('hostel_huptainer.arguments.ArgumentParser')

    Arguments(stub_argv)

    mock_parser.assert_has_calls([
        mocker.call().parse_args(expected_args)])
