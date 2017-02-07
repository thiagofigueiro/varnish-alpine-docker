import dns.resolver
import json
import pytest
import requests
from subprocess import getoutput, run, DEVNULL
from time import sleep


def _get_host_port():
    container_info = json.loads(getoutput('docker inspect varnish-alpine'))[0]
    return int(container_info['NetworkSettings']['Ports']['80/tcp'][0]['HostPort'])


def _get_url(path, port):
    return 'http://localhost:{port}{path}'.format(**locals())


def _request(host, path, port):
    return requests.get(_get_url(path, port), headers={'host': host}, allow_redirects=False)


def _get_response_code(host, path, port):
    r = _request(host, path, port)
    return r.status_code


def _get_headers(host, path, port):
    r = _request(host, path, port)
    return r.headers


def _get_age(host, path, port):
    headers = _get_headers(host, path, port)
    return int(headers['Age'])


def _kill_docker():
    run(['docker', 'rm', '-f', 'varnish-alpine'], stdout=DEVNULL)


def _get_first_address(name):
    answer = dns.resolver.query(name, 'A')
    ip_address = None
    for ip_address in answer:
        break

    return ip_address


def _start_docker(name):
    ip_address = _get_first_address(name)
    run(['docker', 'run', '-Pid', '-e',
         'VARNISH_BACKEND_ADDRESS={}'.format(ip_address), '-e',
         'VARNISH_BACKEND_PORT=80', '--name=varnish-alpine',
         'thiagofigueiro/varnish-alpine-docker:ci'],
        stdout=DEVNULL)
    sleep(1)


class TestInstagram:

    def setup_class(self):
        self.host = 'instagramstatic-a.akamaihd.net'
        _start_docker(self.host)
        self.host_port = _get_host_port()

    def teardown_class(self):
        _kill_docker()

    def test_200_cached(self):
        assert 200 == _get_response_code(
                host=self.host,
                path='/h1/images/appstore-install-badges/english_get.png/74c874cf7dc5.png',
                port=self.host_port)
        sleep(1)
        assert 0 < _get_age(
                host=self.host,
                path='/h1/images/appstore-install-badges/english_get.png/74c874cf7dc5.png',
                port=self.host_port)


class TestGoogle:

    def setup_class(self):
        self.host = 'www.google.com'
        _start_docker(self.host)
        self.host_port = _get_host_port()

    def teardown_class(self):
        _kill_docker()

    def test_host_port(self):
        assert 0 < self.host_port < 65535

    # FIXME: failing in travis-ci
    @pytest.mark.xfail
    def test_302(self):
        assert 302 == _get_response_code(host=self.host, path='/?q=test', port=self.host_port)

    def test_200(self):
        assert 200 == _get_response_code(
                host=self.host,
                path='/images/branding/googlelogo/2x/googlelogo_color_272x92dp.png',
                port=self.host_port)

