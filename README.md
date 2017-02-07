# varnish-alpine-docker
![Build Status](https://api.travis-ci.org/thiagofigueiro/varnish-alpine-docker.svg)
![Docker Stars](https://img.shields.io/docker/stars/thiagofigueiro/varnish-alpine-docker.svg?link=https://hub.docker.com/r/thiagofigueiro/varnish-alpine-docker/)
![Docker Pulls](https://img.shields.io/docker/pulls/thiagofigueiro/varnish-alpine-docker.svg?link=https://hub.docker.com/r/thiagofigueiro/varnish-alpine-docker/)

A Varnish docker container based on Alpine Linux in less than 100MB.

## Environment variables
* `VARNISH_BACKEND_ADDRESS` - host/ip of your backend.  Defaults to 192.168.1.65.
* `VARNISH_BACKEND_PORT` - TCP port of your backend.  Defaults to 80.
* `VARNISH_MEMORY` - how much memory Varnish can use for caching. Defaults to 100M.

## Quick start

Run with defaults:

```bash
docker run -ti --name=varnish-alpine thiagofigueiro/varnish-alpine-docker
```

Specify your backend configuration:

```bash
docker run -e VARNISH_BACKEND_ADDRESS=a.b.c.d -e VARNISH_BACKEND_PORT=nn -ti --name=varnish-alpine thiagofigueiro/varnish-alpine-docker
```

Build image locally:

```bash
git clone git@github.com:thiagofigueiro/varnish-alpine-docker.git
cd varnish-alpine-docker
docker build -t varnish-alpine-docker .
```

## Software

* [Varnish](https://www.varnish-cache.org/)
* [Alpine Linux](https://www.alpinelinux.org/)
* [Docker Alpine](https://github.com/gliderlabs/docker-alpine)

### Versions

The Docker image tag corresponds to the Alpine Linux version used.  The Varnish
version used is whatever Alpine have packaged.

| Image tag | Alpine Version | Varnish version |
|-----------|----------------|-----------------|
| 3.3 | [3.3.3](http://www.alpinelinux.org/posts/Alpine-3.3.3-released.html) | [4.1.2-r1](https://pkgs.alpinelinux.org/packages?name=varnish&branch=v3.3)
| 3.4 | [3.4.6](https://www.alpinelinux.org/posts/Alpine-3.4.6-released.html) | [4.1.2-r3](https://pkgs.alpinelinux.org/packages?name=varnish&branch=v3.4)

## Acknowledgements
* https://github.com/jacksoncage/varnish-docker
