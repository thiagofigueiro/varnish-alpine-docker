import dns.resolver
import json
import pytest
import requests
from subprocess import getoutput, run, DEVNULL
from time import sleep


def _get_host_port():
    container_info = json.loads(getoutput('docker inspect varnish-alpine'))[0]
    return int(container_info['NetworkSettings']['Ports']['80/tcp'][0]['HostPort'])


def _kill_docker():
    run(['docker', 'rm', '-f', 'varnish-alpine'], stdout=DEVNULL)


def _get_first_address(name):
    answer = dns.resolver.query(name, 'A')
    ip_address = None
    for ip_address in answer:
        break

    return ip_address


class DockerTest:

    def __init__(self, host):
        self.host = host
        self._start_docker()
        self.host_port = _get_host_port()

    def close(self):
        _kill_docker()

    def __exit__(self):
        self.close()

    def __del__(self):
        self.close()

    def _start_docker(self):
        ip_address = _get_first_address(self.host)
        run(['docker', 'run', '-Pid', '-e',
             'VARNISH_BACKEND_ADDRESS={}'.format(ip_address), '-e',
             'VARNISH_BACKEND_PORT=80', '--name=varnish-alpine',
             'thiagofigueiro/varnish-alpine-docker:ci'],
            stdout=DEVNULL)
        sleep(1)

    def _request(self, path):
        return requests.get(
            self._get_url(path),
            headers={'host': self.host},
            allow_redirects=False)

    def _get_response_code(self, path):
        r = self._request(path)
        return r.status_code

    def _get_url(self, path):
        return 'http://localhost:{}{}'.format(self.host_port, path)

    def _get_headers(self, path):
        r = self._request(path)
        return r.headers

    def _get_age(self, path):
        headers = self._get_headers(path)
        return int(headers['Age'])


class TestInstagram:
    def setup_class(self):
        self.docker_test = DockerTest('instagramstatic-a.akamaihd.net')

    def teardown_class(self):
        self.docker_test.close()

    def test_200_cached(self):
        assert 200 == self.docker_test._get_response_code(
                '/h1/images/appstore-install-badges/english_get.png/74c874cf7dc5.png')
        sleep(1)
        assert 0 < self.docker_test._get_age(
                '/h1/images/appstore-install-badges/english_get.png/74c874cf7dc5.png')


class TestGoogle:
    def setup_class(self):
        self.docker_test = DockerTest('www.google.com')

    def teardown_class(self):
        del self.docker_test

    def test_host_port(self):
        assert 0 < self.docker_test.host_port < 65535

    def test_302(self):
        assert 302 == self.docker_test._get_response_code('/images')

    def test_200(self):
        assert 200 == self.docker_test._get_response_code(
                '/images/branding/googlelogo/2x/googlelogo_color_272x92dp.png')

