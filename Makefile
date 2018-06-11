# @Author: bsuttor
# @Date:   2018-06-11T16:29:42+02:00
# @Last modified by:   bsuttor
# @Last modified time: 2018-06-11T16:33:31+02:00



#!/usr/bin/make
ifeq (rsync,$(firstword $(MAKECMDGOALS)))
  # use the rest as arguments for "rsync"
  RSYNC_ARGS := $(wordlist 2,$(words $(MAKECMDGOALS)),$(MAKECMDGOALS))
  # ...and turn them into do-nothing targets
  $(eval $(RSYNC_ARGS):;@:)
endif

VERSION=`cat version.txt`
#BUILD_NUMBER := debug1
UID := $(shell id -u)
PROJECTID := $(shell basename "${PWD}")
RSYNC_ARGS :=  $(if $(RSYNC_ARGS),$(RSYNC_ARGS),"a")

all: run

buildout.cfg:
	ln -fs dev.cfg buildout.cfg
	#ln -fs prod.cfg buildout.cfg

bin/buildout: buildout.cfg
	python bootstrap.py --buildout-version=2.11.3 --setuptools-version=38.7.0

.PHONY: robot-server
robot-server:
	bin/robot-server -v cpskin.policy.testing.CPSKIN_POLICY_ROBOT_TESTING

stop-old:
	docker rm -f $$(docker ps -a | grep "_zeo_" | awk '{print $$1}')
	docker rm -f $$(docker ps -a | grep "_instance_" | awk '{print $$1}')
	docker rm -f $$(docker ps -a | grep "_reverseproxy_" | awk '{print $$1}')

.PHONY: run
run: build
	make up

.PHONY: cleanall
cleanall:
	rm -fr develop-eggs downloads eggs parts .installed.cfg lib include bin .mr.developer.cfg .env traefik.toml local/ var/instance/minisites/*
	docker-compose down

docker-image:
	docker build --pull -t docker-staging.imio.be/iasmartweb/mutual:latest .

buildout-prod: bin/buildout
    # used in docker build
	pip install --user -I -r requirements.txt
	~/.local/bin/buildout -t 22 -c prod.cfg

var/instance/minisites:
	mkdir -p var/instance/minisites

.env:
	echo uid=${UID} > .env
	python scripts/config.py --serverinfos

env: .env

var/blobstorage:
	mkdir -p var/blobstorage

var/filestorage:
	mkdir -p var/filestorage

src:
	mkdir src

build: .env buildout.cfg minisites var/blobstorage var/blobstorage src
	# rm -rf local/ bin/
	docker-compose build --pull zeo # <--no-cache
	make buildout

buildout:
	# docker-compose run --rm zeo bin/develop checkout .
	docker-compose run --rm instance bash -c "virtualenv . && bin/pip install -I -r requirements.txt && bin/buildout -c docker-dev.cfg"

upgrade: .env var/instance/minisites
	docker-compose run --rm --service-ports instance bin/upgrade-portals

# bin/instance:
	# make build

up: .env var/instance/minisites
	docker-compose run --rm --service-ports --name instance instance

bash: .env var/instance/minisites
	docker-compose run --rm --service-ports instance bash

install-docker-compose:
	sudo curl -L https://github.com/docker/compose/releases/download/1.19.0/docker-compose-`uname -s`-`uname -m` -o /usr/local/bin/docker-compose

dev:
	ln -fs dev.cfg buildout.cfg
	virtualenv-2.7 .
	./bin/pip install -r requirements.txt
	./bin/buildout

rsync: .env
	python scripts/config.py --rsync $(RSYNC_ARGS)

minisites: .env var/instance/minisites
	python scripts/config.py --minisitesfiles
