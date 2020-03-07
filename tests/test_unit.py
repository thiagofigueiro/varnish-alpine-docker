import dns.resolver
import json
import requests
from subprocess import getoutput, run, DEVNULL
from time import sleep, time
from urllib3.exceptions import HTTPError

TIMEOUT = 10  # seconds


def _get_first_address(name):
    answer = dns.resolver.query(name, 'A')
    ip_address = None
    for ip_address in answer:
        break

    return ip_address


class DockerTest:
    def __init__(self, host):
        self.host = host
        self.container_name = 'varnish-alpine-' + str(time())
        self._start_docker()
        self.host_port = self._get_host_port()
        self._wait_for_varnish()

    def close(self):
        run(['docker', 'rm', '-f', self.container_name], stdout=DEVNULL)

    def _get_host_port(self):
        container_info = json.loads(getoutput('docker inspect ' + self.container_name))[0]
        try:
            return int(container_info['NetworkSettings']['Ports']['80/tcp'][0]['HostPort'])
        except KeyError:
            raise RuntimeError('Varnish container not listening on 80/tcp') from None

    def __exit__(self):
        self.close()

    def __del__(self):
        self.close()

    def _wait_for_varnish(self):
        elapsed_time = 0
        ready = False
        print(f'Waiting {TIMEOUT}s for varnish to be available')
        while elapsed_time < TIMEOUT and not ready:
            try:
                response_code = self._get_response_code('/')
                if response_code in (200, 301, 404):
                    ready = True
            except (ConnectionRefusedError, ConnectionError, IOError, HTTPError):
                print(elapsed_time)
                pass
            sleep(1)
            elapsed_time += 1

        if not ready:
            raise RuntimeError(f'Timeout waiting for varnish on {self._get_host_port()}')

    def _start_docker(self):
        ip_address = _get_first_address(self.host)
        run(['docker', 'run', '-Pid', '-e',
             'VARNISH_BACKEND_ADDRESS={}'.format(ip_address), '-e',
             'VARNISH_BACKEND_PORT=80', '--name=' + self.container_name,
             'thiagofigueiro/varnish-alpine-docker:ci'],
            stdout=DEVNULL)
        sleep(1)

    def _request(self, path, **kwargs):
        _kwargs = {
            'headers': {'host': self.host},
            'allow_redirects': False,
        }
        _kwargs.update(kwargs)

        r = requests.get(
            self._get_url(path),
            **_kwargs,
        )
        return r

    def _get_response_code(self, path, **kwargs):
        r = self._request(path, **kwargs)
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
        self.docker_test = DockerTest('www.instagram.com')

    def teardown_class(self):
        self.docker_test.close()

    def test_200_cached(self):
        assert 200 == self.docker_test._get_response_code(
                '/static/images/homepage/screenshot1-2x.jpg/2debbd5aaab8.jpg',
                allow_redirects=True,
        )
        sleep(1)
        assert 0 < self.docker_test._get_age(
                '/static/images/homepage/screenshot1-2x.jpg/2debbd5aaab8.jpg')


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

