"""Tests the hostel_huptainer.containers module."""

# Hack implementation:
#
# import docker
# client = docker.client.DockerClient()
# client.containers.list(filters={'label': 'org.eff.certbot.cert_cns', 'status': 'running'})
# for container in containers:
#     cn_list = container.labels['org.eff.certbot.cert_cns']
#     for host in cn_list.split(','):
#         if hostname == host.strip():
#             yield container

import pytest

from hostel_huptainer.containers import MatchingContainers


@pytest.mark.parametrize('label', ['thing1.com', 'arm1.thing2.com'])
def test_properly_initializes_label_value(mocker, label):
    mocker.patch('hostel_huptainer.containers.docker')

    matching_containers = MatchingContainers(label)

    assert matching_containers.label_value == label


def test_properly_initializes_docker_client(mocker):
    stub_client = mocker.MagicMock()
    mocker.patch('hostel_huptainer.containers.docker.client.DockerClient',
                 return_value=stub_client)

    matching_containers = MatchingContainers(None)

    assert matching_containers.docker == stub_client


@pytest.mark.skip('to be tackled later')
def test___iter___properly_passes_filter_to_container_list_method():
    pytest.fail('test not written yet')


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
