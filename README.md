# varnish-alpine-docker
[![Build Status](https://api.travis-ci.org/thiagofigueiro/varnish-alpine-docker.svg)](https://travis-ci.org/thiagofigueiro/varnish-alpine-docker)
[![Docker Stars](https://img.shields.io/docker/stars/thiagofigueiro/varnish-alpine-docker.svg)](https://hub.docker.com/r/thiagofigueiro/varnish-alpine-docker/)
[![Docker Pulls](https://img.shields.io/docker/pulls/thiagofigueiro/varnish-alpine-docker.svg)](https://hub.docker.com/r/thiagofigueiro/varnish-alpine-docker/)

A very small Varnish docker image based on Alpine Linux.

## Environment variables
* `VARNISH_BACKEND_ADDRESS` - host/ip of your backend.  Defaults to 192.168.1.65.
* `VARNISH_BACKEND_PORT` - TCP port of your backend.  Defaults to 80.
* `VARNISH_MEMORY` - how much memory Varnish can use for caching. Defaults to 100M.

## Quick start

Run with defaults:

```bash
docker run -Pit --name=varnish-alpine thiagofigueiro/varnish-alpine-docker
```

Specify your backend configuration:

```bash
docker run -e VARNISH_BACKEND_ADDRESS=a.b.c.d \
           -e VARNISH_BACKEND_PORT=nn \
           -e VARNISH_MEMORY=1G \
           -Pit --name=varnish-alpine thiagofigueiro/varnish-alpine-docker
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
| latest | [3.7.0](https://www.alpinelinux.org/posts/Alpine-3.7.0-released.html) | [5.2.1-r0](https://pkgs.alpinelinux.org/packages?name=varnish&branch=v3.7)
| 3.7 | [3.7.0](https://www.alpinelinux.org/posts/Alpine-3.7.0-released.html) | [5.2.1-r0](https://pkgs.alpinelinux.org/packages?name=varnish&branch=v3.7)
| 3.6 | [3.6.0](https://www.alpinelinux.org/posts/Alpine-3.6.0-released.html) | [4.1.9-r0](https://pkgs.alpinelinux.org/packages?name=varnish&branch=v3.6)
| 3.5 | [3.5.0](https://www.alpinelinux.org/posts/Alpine-3.5.0-released.html) | [4.1.3-r0](https://pkgs.alpinelinux.org/packages?name=varnish&branch=v3.5)
| 3.4 | [3.4.6](https://www.alpinelinux.org/posts/Alpine-3.4.6-released.html) | [4.1.2-r3](https://pkgs.alpinelinux.org/packages?name=varnish&branch=v3.4)
| 3.3 | [3.3.3](http://www.alpinelinux.org/posts/Alpine-3.3.3-released.html) | [4.1.2-r1](https://pkgs.alpinelinux.org/packages?name=varnish&branch=v3.3)

## Acknowledgements
* https://github.com/jacksoncage/varnish-docker
