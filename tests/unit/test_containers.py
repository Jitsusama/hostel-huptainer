"""Tests the hostel_huptainer.containers module."""

try:
    import unittest.mock as mock
except ImportError:
    import mock
import docker.errors
import pytest
from hostel_huptainer.errors import ContainerError

from hostel_huptainer.containers import (
    MatchingContainers, csv_contains_value, send_signal)


class TestCsvContains(object):
    @pytest.mark.parametrize('csv_string', [
        'match',
        'no_match,match,notta',
        'no match, match, notta, same here'])
    def test_returns_true_on_match(self, csv_string):
        result = csv_contains_value(csv_string, 'match')

        assert result

    @pytest.mark.parametrize('csv_string', [
        'nomatch',
        'no_match,stillnomatch,notta',
        'no match, menomatchmatch, notta, same here'])
    def test_returns_false_when_no_match_found(self, csv_string):
        result = csv_contains_value(csv_string, 'match')

        assert not result


class TestSendSignal(object):
    def test_properly_sends_sighup_when_requested(self, mocker):
        mock_container = mocker.MagicMock()

        send_signal('reload', mock_container)

        mock_container.assert_has_calls([mocker.call.kill(signal="SIGHUP")])

    def test_properly_restarts_when_requested(self, mocker):
        mock_container = mocker.MagicMock()

        send_signal('restart', mock_container)

        mock_container.assert_has_calls([mocker.call.restart()])


class TestMatchingContainersInit(object):
    @pytest.mark.parametrize('label', ['thing1.com', 'arm1.thing2.com'])
    def test_properly_sets_label_value(self, mocker, label):
        mocker.patch('hostel_huptainer.containers.docker')

        containers = MatchingContainers(label)

        assert containers.label_value == label


class TestMatchingContainersIter(object):
    def test_properly_passes_filter_to_container_list_method(self, mocker):
        stub_client = mocker.MagicMock()
        stub_client.return_value.containers.list.return_value = [
            mocker.MagicMock()]
        mocker.patch('hostel_huptainer.containers.csv_contains_value')
        mock_docker = mocker.patch(
            'hostel_huptainer.containers.docker.client',
            DockerClient=stub_client)

        list(MatchingContainers(None))

        expected_dict = {
            'label': 'org.eff.certbot.cert_cns',
            'status': 'running'}
        mock_docker.assert_has_calls([
            mocker.call.DockerClient().containers.list(filters=expected_dict)])

    @pytest.mark.parametrize('mock_list', [
        [mock.MagicMock()],
        [mock.MagicMock(), mock.MagicMock()]])
    def test_accesses_host_label_for_each_container(
            self, mocker, mock_list):
        stub_client = mocker.MagicMock()
        stub_client.return_value.containers.list.return_value = mock_list
        mocker.patch('hostel_huptainer.containers.docker.client',
                     DockerClient=stub_client)
        mocker.patch('hostel_huptainer.containers.csv_contains_value')

        list(MatchingContainers('stub-host.fqdn'))

        for mock_item in mock_list:
            mock_item.assert_has_calls([
                mocker.call.labels.get('org.eff.certbot.cert_cns')])

    @pytest.mark.parametrize('label_list', [
        'stub-host.fqdn', 'stub-host.fqdn, stubby-host.fqdn'])
    def test_passes_label_string_to_csv_contains_value(
            self, mocker, label_list):
        stub_item = mocker.MagicMock()
        stub_item.labels.get = lambda _: label_list
        stub_container_list = [stub_item, stub_item]
        stub_client = mocker.MagicMock()
        stub_client.return_value.containers.list.return_value = (
            stub_container_list)
        mocker.patch(
            'hostel_huptainer.containers.docker.client',
            DockerClient=stub_client)
        mock_contains = mocker.patch(
            'hostel_huptainer.containers.csv_contains_value')

        _ = [item for item in MatchingContainers('stub-host.fqdn')]

        for _ in stub_container_list:
            mock_contains.assert_called_with(label_list, 'stub-host.fqdn')

    def test___iter___yields_matching_containers(
            self, mocker):
        stub_item = mocker.MagicMock()
        stub_item.labels.get = lambda _: 'stub-host.fqdn'
        stub_container_list = [stub_item]
        stub_client = mocker.MagicMock()
        stub_client.return_value.containers.list.return_value = (
            stub_container_list)
        mocker.patch(
            'hostel_huptainer.containers.docker.client',
            DockerClient=stub_client)

        matching_containers = MatchingContainers('stub-host.fqdn')

        assert stub_item in list(matching_containers)

    def test___iter___does_not_yield_mismatching_containers(
            self, mocker):
        stub_item = mocker.MagicMock()
        stub_item.labels.get = lambda _: 'no-match.fqdn'
        stub_container_list = [stub_item]
        stub_client = mocker.MagicMock()
        stub_client.return_value.containers.list.return_value = (
            stub_container_list)
        mocker.patch(
            'hostel_huptainer.containers.docker.client',
            DockerClient=stub_client)

        matching_containers = MatchingContainers('stub-host.fqdn')

        assert stub_item not in list(matching_containers)

    def test_raises_error_when_docker_api_error_encountered(
            self, mocker):
        stub_client = mocker.MagicMock(
            side_effect=docker.errors.APIError(None))
        mocker.patch(
            'hostel_huptainer.containers.docker.client',
            DockerClient=stub_client)

        with pytest.raises(ContainerError):
            list(MatchingContainers(None))

    def test_error_encapsulates_docker_api_error_message(
            self, mocker):
        stub_client = mocker.MagicMock(
            side_effect=docker.errors.APIError("stub-message"))
        mocker.patch(
            'hostel_huptainer.containers.docker.client',
            DockerClient=stub_client)

        with pytest.raises(ContainerError) as error:
            list(MatchingContainers(None))

        assert "stub-message" in str(error)
