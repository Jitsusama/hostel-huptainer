"""Tests the hostel_huptainer.containers module."""

# Hack implementation:
#
# import docker
# client = docker.client.DockerClient()
# client.containers.list(filters={'label': 'org.eff.certbot.cert_cns', 'status': 'running'})
# for container in containers:
#     cn_list = container.labels.get('org.eff.certbot.cert_cns')
#     if not cn_list:
#         raise NoMatchesFound()
#     if any([host.strip() == 'test-host' for host in cn_list.split(',')]):
#         yield container
#     else:
#         raise NoMatchesFound()

import pytest

from hostel_huptainer.containers import MatchingContainers, csv_contains_value


@pytest.mark.parametrize('csv_string', [
    'match',
    'no_match,match,notta',
    'no match, match, notta, same here'])
def test_csv_contains_value_returns_true_on_match(csv_string):
    result = csv_contains_value(csv_string, 'match')

    assert result


@pytest.mark.parametrize('csv_string', [
    'nomatch',
    'no_match,stillnomatch,notta',
    'no match, menomatchmatch, notta, same here'])
def test_csv_contains_value_returns_false_when_no_match_found(csv_string):
    result = csv_contains_value(csv_string, 'match')

    assert not result


@pytest.mark.parametrize('label', ['thing1.com', 'arm1.thing2.com'])
def test_properly_initializes_label_value(mocker, label):
    mocker.patch('hostel_huptainer.containers.docker')

    containers = MatchingContainers(label)

    assert containers.label_value == label


def test_properly_initializes_docker_client(mocker):
    stub_client = mocker.MagicMock()
    mocker.patch('hostel_huptainer.containers.docker.client.DockerClient',
                 return_value=stub_client)

    containers = MatchingContainers(None)

    assert containers.docker == stub_client


def test___iter___properly_passes_filter_to_container_list_method(mocker):
    mock_docker = mocker.patch('hostel_huptainer.containers.docker.client')

    containers = MatchingContainers(None)
    iterator = iter(containers)
    next(iterator)

    expected_dict = {'label': 'org.eff.certbot.cert_cns', 'status': 'running'}
    mock_docker.assert_has_calls([
        mocker.call.DockerClient().containers.list(filters=expected_dict)])


def test___iter___passes_label_string_to_csv_contains_value(mocker):
    stub_mocks = [mocker.MagicMock(), mocker.MagicMock()]
    stub_list = mocker.MagicMock(return_value=stub_mocks)
    stub_client = mocker.MagicMock()
    stub_client.return_value.containers = mocker.MagicMock(list=stub_list)
    mocker.patch(
        'hostel_huptainer.containers.docker.client',
        DockerClient=stub_client)
    mock_contains = mocker.patch(
        'hostel_huptainer.containers.csv_contains_value')

    containers = MatchingContainers('stub-host.fqdn')
    iterator = iter(containers)
    next(iterator)

    mock_contains.assert_called_once_with(stub_mocks, 'stub-host.fqdn')


@pytest.mark.skip('to be tackled later')
def test___iter___only_yields_matching_containers():
    pytest.fail('test not written yet')


@pytest.mark.skip('to be tackled later')
def test_raises_no_matches_error_when_no_containers_match():
    pytest.fail('test not written yet.')


@pytest.mark.skip('to be tackled later')
def test_no_matches_error_states_when_no_matches_found():
    pytest.fail('test not written yet')


@pytest.mark.skip('to be tackled later')
def test_raises_no_matches_error_when_docker_api_error_encountered():
    pytest.fail('test not written yet.')


@pytest.mark.skip('to be tackled later')
def test_no_matches_error_states_when_docker_api_issue_encountered():
    pytest.fail('test not written yet')
