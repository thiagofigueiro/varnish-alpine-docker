#!/bin/sh

mkdir -p /var/lib/varnish/`hostname` && chown nobody /var/lib/varnish/`hostname`
if [ -n "${VARNISH_CONFIG_FILE}" ]; then
  varnishd -s malloc,${VARNISH_MEMORY} -a :80 -f ${VARNISH_CONFIG_FILE}
else
  varnishd -s malloc,${VARNISH_MEMORY} -a :80 -b ${VARNISH_BACKEND_ADDRESS}:${VARNISH_BACKEND_PORT}
fi

sleep 1
varnishlog
