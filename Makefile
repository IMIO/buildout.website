#!/usr/bin/make
# UID := $(shell id -u)
# docker build args to add after tests: --no-cache --force-rm
iasmartweb-build-cache:
	docker build --pull --build-arg repo=buildout.website -t docker-staging.imio.be/iasmartweb/cache:latest .

