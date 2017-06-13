"""Test hostel_huptainer.environment module."""

import pytest
from hostel_huptainer.errors import InputError

from hostel_huptainer.environment import Environment


def test_checks_passed_dict_for_certbot_hostname_key(mocker):
    mock_dict = mocker.MagicMock()

    Environment(mock_dict)

    mock_dict.assert_has_calls([mocker.call.get('CERTBOT_HOSTNAME')])


def test_throws_input_error_when_certbot_hostname_isnt_present():
    stub_dict = {}

    with pytest.raises(InputError):
        Environment(stub_dict)


def test_input_error_includes_message_about_certbot_hostname_missing():
    stub_dict = {}

    with pytest.raises(InputError) as error:
        Environment(stub_dict)

    assert 'CERTBOT_HOSTNAME' in str(error)


@pytest.mark.parametrize('example_hostname', ['george.com', 'sam.edu'])
def test_stores_certbot_hostname(example_hostname):
    stub_dict = {'CERTBOT_HOSTNAME': example_hostname}

    environment = Environment(stub_dict)

    assert environment.hostname == example_hostname
