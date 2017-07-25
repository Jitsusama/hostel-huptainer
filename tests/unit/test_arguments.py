"""Tests the hostel_huptainer.arguments module."""

import pytest

from hostel_huptainer.arguments import Arguments


def test_passes_usage_information_to_argumentparser(mocker):
    mock_parser = mocker.patch(
        'hostel_huptainer.arguments.ArgumentParser')

    Arguments(['hostel-huptainer'])

    mock_parser.assert_called_once_with(
        description=mocker.ANY, epilog=mocker.ANY)


@pytest.mark.parametrize('stub_argv, expected_args', [
    (['hostel-huptainer', '-a', '-b'], ['-a', '-b']),
    (['hostel-huptainer', '--help'], ['--help']),
    (['hostel-huptainer'], []),
])
def test_passes_arguments_and_not_progname_to_parse_args(
        mocker, stub_argv, expected_args):
    mock_parser = mocker.patch(
        'hostel_huptainer.arguments.ArgumentParser')

    Arguments(stub_argv)

    mock_parser.assert_has_calls([
        mocker.call().parse_args(expected_args)])


@pytest.mark.parametrize('version', ['v0.0.1', 'v1.2.3'])
def test_passes_version_details_to_add_argument_before_parsing(
        mocker, version):
    stub_version = mocker.patch(
        'hostel_huptainer.arguments.__version__', value=version)
    mock_parser = mocker.patch(
        'hostel_huptainer.arguments.ArgumentParser')

    Arguments(['hostel-huptainer'])

    mock_parser.assert_has_calls([
        mocker.call().add_argument(
            '-v', '--version', action='version', version=stub_version),
        mocker.call().parse_args(mocker.ANY)])


def test_properly_adds_signal_argument_to_argument_parser(
        mocker):
    mock_parser = mocker.patch(
        'hostel_huptainer.arguments.ArgumentParser')

    Arguments(['hostel-huptainer'])

    mock_parser.assert_has_calls([
        mocker.call().add_argument(
            '-s', '--signal', dest='signal_method', default='reload',
            choices=['reload', 'restart'], help=mocker.ANY)])


@pytest.mark.parametrize('signal_method', ['reload', 'restart'])
def test___getattr___grabs_parsed_namespace_attributes(mocker, signal_method):
    stub_parser = mocker.patch(
        'hostel_huptainer.arguments.ArgumentParser')
    stub_parser.return_value.parse_args.return_value.__getattribute__ \
        = lambda _: signal_method

    arguments = Arguments(['hostel-huptainer', '--signal', signal_method])

    assert arguments.__getattr__('signal_method') == signal_method
