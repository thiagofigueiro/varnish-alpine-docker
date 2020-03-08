"""Integration tests for varnish-alpine-docker"""
import os
import requests
from time import sleep
from urllib3.exceptions import HTTPError

VARNISH_BACKEND_HOSTNAME = os.environ['VARNISH_BACKEND_HOSTNAME']
SERVICE_HOST = os.environ.get('SERVICE_HOST', 'varnish-alpine-docker')
SERVICE_PORT = os.environ.get('SERVICE_PORT', 80)
TIMEOUT = 10  # seconds


class VarnishTest:
    """Small HTTP client to test varnish a backend"""
    def __init__(self,
                 host=VARNISH_BACKEND_HOSTNAME,
                 varnish_host=SERVICE_HOST,
                 varnish_port=SERVICE_PORT):
        self.host = host
        self.varnish_host = varnish_host
        self.varnish_port = int(varnish_port)
        self._wait_for_varnish()

    def _wait_for_varnish(self):
        elapsed_time = 0
        ready = False
        print(f'Waiting {TIMEOUT}s for varnish to be available')
        while elapsed_time < TIMEOUT and not ready:
            try:
                response_code = self.get_response_code('/')
                if response_code in (200, 301, 404):
                    ready = True
            except (ConnectionRefusedError, ConnectionError, IOError, HTTPError):
                print(elapsed_time)

            sleep(1)
            elapsed_time += 1

        if not ready:
            raise RuntimeError(
                f'Timeout waiting for varnish on {self.varnish_host}:{self.varnish_port}')

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

    def get_response_code(self, path, **kwargs):
        r = self._request(path, **kwargs)
        return r.status_code

    def _get_url(self, path):
        return f'http://{self.varnish_host}:{self.varnish_port}{path}'

    def _get_headers(self, path):
        r = self._request(path)
        return r.headers

    def get_age(self, path):
        headers = self._get_headers(path)
        return int(headers['Age'])


class TestInstagram:
    def setup_class(self):
        self.varnish = VarnishTest('www.instagram.com')

    def test_200_cached(self):
        assert 200 == self.varnish.get_response_code(
            '/static/images/homepage/screenshot1-2x.jpg/2debbd5aaab8.jpg',
            allow_redirects=True,
        )
        sleep(1)
        assert 0 < self.varnish.get_age(
            '/static/images/homepage/screenshot1-2x.jpg/2debbd5aaab8.jpg')


class TestGoogle:
    def setup_class(self):
        self.varnish = VarnishTest('www.google.com')

    def test_302(self):
        assert 302 == self.varnish.get_response_code('/images')

    def test_200(self):
        assert 200 == self.varnish.get_response_code(
            '/images/branding/googlelogo/2x/googlelogo_color_272x92dp.png')
