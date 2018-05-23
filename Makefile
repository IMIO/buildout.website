#!/usr/bin/make
# UID := $(shell id -u)
# docker build args to add after tests: --no-cache --force-rm
iasmartweb-build-cache:
	docker build --no-cache --force-rm --pull --build-arg repo=buildout.website --build-arg cmd='/usr/bin/python bootstrap.py -c prod.cfg && make buildout-prod' -t docker-staging.imio.be/iasmartweb/cache:latest .
