FROM alpine:3.10
LABEL maintainer="https://github.com/thiagofigueiro/varnish-alpine-docker"
LABEL refreshed_at=2019-12-08
ENV VARNISH_BACKEND_ADDRESS 192.168.1.65
ENV VARNISH_MEMORY 100M
ENV VARNISH_BACKEND_PORT 80
EXPOSE 80

RUN apk update && \
    apk upgrade && \
    apk add varnish

ADD start.sh /start.sh
CMD ["/start.sh"]
