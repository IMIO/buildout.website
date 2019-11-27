# @Author: bsuttor
# @Date:   2018-06-11T16:29:42+02:00
# @Last modified by:   bsuttor
# @Last modified time: 2018-06-11T16:49:39+02:00



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
	docker stop $$(docker ps -q)
	docker rm $$(docker ps -a -q)

.PHONY: run
run: build
	make up

.PHONY: cleanall
cleanall:
	rm -fr develop-eggs downloads eggs parts .installed.cfg lib include bin .mr.developer.cfg .env traefik.toml local/ var/instance/minisites/* __pycache__
	docker-compose down

docker-image:
	docker build --pull -t iasmartweb/mutual:latest .

buildout-prod:
    # used in docker build
	pip install --user -I -r requirements.txt
	~/.local/bin/buildout -t 30 -c prod.cfg

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

build: .env buildout.cfg minisites var/blobstorage var/filestorage src
	# rm -rf local/ bin/
	docker-compose build --pull zeo # <--no-cache
	make buildout

buildout:
	# docker-compose run --rm zeo bin/develop checkout .
	docker-compose run --rm instance bash -c "virtualenv . && bin/pip install -I -r requirements.txt && bin/buildout -c docker-dev.cfg"

upgrade: .env var/instance/minisites
	docker-compose run --rm instance bin/upgrade-portals

up: .env var/instance/minisites
	# docker-compose run --rm --service-ports instance
	docker-compose up

bash: .env var/instance/minisites
	docker-compose run --rm -p 8081:8081 --name instance instance bash

restart-instance-only:
	docker-compose up -d --force-recreate --no-deps instance

dev:
	ln -fs dev.cfg buildout.cfg
	if [ -f /usr/bin/virtualenv-2.7 ] ; then virtualenv-2.7 .;else virtualenv -p python2.7 .;fi
	./bin/pip install -r requirements.txt
	./bin/buildout -t 30

rsync: .env var/blobstorage var/filestorage
	./bin/python scripts/config.py --rsync $(RSYNC_ARGS)

minisites: .env var/instance/minisites
	./bin/python scripts/config.py --minisitesfiles

develop-up:
	docker-compose run --rm instance bin/develop up

p3:
	virtualenv -p python3 p3

p3/bin/pytest: p3
	p3/bin/pip install -r tests/requirements.txt

test-starting: p3/bin/pytest
	./p3/bin/pytest -s tests
