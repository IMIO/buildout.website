#!/usr/bin/make
# @Author: bsuttor
# @Date:   2018-06-11T16:29:42+02:00
# @Last modified by:   bsuttor
# @Last modified time: 2018-06-11T16:49:39+02:00

IMAGE_NAME="docker-staging.imio.be/iasmartweb/mutual:latest"

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

bin/pip:
	if [ -f /usr/bin/virtualenv-2.7 ] ; then virtualenv-2.7 .;else virtualenv -p python2.7 .;fi

bin/buildout: buildout.cfg
	./bin/pip install -r requirements.txt

dev: buildout.cfg bin/pip bin/buildout
	./bin/buildout -Nt 30

.PHONY: robot-server
robot-server:
	bin/robot-server -v cpskin.policy.testing.CPSKIN_POLICY_ROBOT_TESTING

.PHONY: cleanall
cleanall:
	rm -fr develop-eggs downloads eggs parts .installed.cfg lib include bin .mr.developer.cfg .env traefik.toml local/ var/instance/minisites/* __pycache__
	docker-compose down

var/instance/minisites:
	mkdir -p var/instance/minisites

.env:
	echo uid=${UID} > .env
	python scripts/config.py --serverinfos

env: .env

### DOCKER ###
.PHONY: run
run: build
	$(MAKE) up

docker-image:
	docker build --pull -t iasmartweb/mutual:latest .

var/blobstorage:
	mkdir -p var/blobstorage

var/filestorage:
	mkdir -p var/filestorage

build:
	# rm -rf local/ bin/
	docker-compose build --pull zeo # <--no-cache
	make buildout

buildout:
	# docker-compose run --rm zeo bin/develop checkout .
	docker-compose run --rm instance bash -c "virtualenv . && bin/pip install -I -r requirements.txt && bin/buildout -c docker-dev.cfg"

upgrade: .env var/instance/minisites
	docker-compose run --rm instance bin/upgrade-portals

docker-permissions:
	docker-compose run --rm -u root zeo chown -R imio:imio /home/imio/imio-website/var

up: minisites var/instance/minisites docker-permissions
	# docker-compose run --rm --service-ports instance
	docker-compose up

bash: .env var/instance/minisites
	docker-compose run --rm -p 8081:8081 --name instance instance bash

rsync: bin/pip .env var/blobstorage var/filestorage
	./bin/python scripts/config.py --rsync $(RSYNC_ARGS)

minisites: .env var/instance/minisites bin/python
	./bin/python scripts/config.py --minisitesfiles

eggs:  ## Copy eggs from docker image to speed up docker build
	-docker run --entrypoint='' $(IMAGE_NAME) tar -c -C /home/imio/imio-website eggs | tar x
	##-docker run --entrypoint='' $(IMAGE_NAME) tar -c -C /home/imio/.buildout eggs | tar x
	mkdir -p eggs

### Locust testing ###
p3:
	virtualenv -p python3 p3

p3/bin/pytest: p3
	p3/bin/pip install -r tests/requirements.txt

test-starting: p3/bin/pytest
	./p3/bin/pytest -s tests
