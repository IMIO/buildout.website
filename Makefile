#!/usr/bin/make
#
all: run
VERSION=`cat version.txt`
#BUILD_NUMBER := debug1
UID := $(shell id -u)
PROJECTID := $(shell basename "${PWD}")

buildout.cfg:
	ln -fs dev.cfg buildout.cfg
	#ln -fs prod.cfg buildout.cfg

bin/buildout: buildout.cfg
	python bootstrap.py

.PHONY: buildout
buildout:
	make build

.PHONY: robot-server
robot-server:
	bin/robot-server -v cpskin.policy.testing.CPSKIN_POLICY_ROBOT_TESTING

.PHONY: run
run: build
	make up

.PHONY: cleanall
cleanall:
	rm -fr develop-eggs downloads eggs parts .installed.cfg lib include bin .mr.developer.cfg .env nginx.conf rsync.sh
	docker-compose down

docker-image:
	docker build -t docker-staging.imio.be/iasmartweb/mutual:latest .

buildout-prod: bin/buildout
    # used in docker build
	bin/buildout -t 22 -c prod.cfg

var/instance/minisites:
	mkdir -p var/instance/minisites

minisites-conf:
	scripts/minisites-conf.py --projectid ${PROJECTID}

.env:
	echo uid=${UID} > .env
	echo projectid=${PROJECTID} >> .env

build: .env
	docker-compose pull
	docker-compose run zeo /usr/bin/python bootstrap.py -c docker-dev.cfg
	docker-compose run zeo bin/buildout -c docker-dev.cfg

up: .env var/instance/minisites
	docker-compose up

install-docker-compose:
	sudo curl -L https://github.com/docker/compose/releases/download/1.19.0/docker-compose-`uname -s`-`uname -m` -o /usr/local/bin/docker-compose

rsync.shq:
	echo "#!/bin/bash" > rsync.sh
	echo "rsync -P imio@`curl -s -H 'Content-Type: application/json' http://infra-api.imio.be/application/${PROJECTID}/website/production | python -c "import sys, json; print json.load(sys.stdin)[0]['server_name']")`:/srv/instances/${PROJECTID}/filestorage/Data.fs var/filestorage/Data.fs" >> rsync.sh
	echo "rsync -r --info=progress2 imio@`curl -s -H 'Content-Type: application/json' http://infra-api.imio.be/application/${PROJECTID}/website/production | python -c "import sys, json; print json.load(sys.stdin)[0]['server_name']")`:/srv/instances/${PROJECTID}/blobstorage/ var/blobstorage/" >> rsync.sh
	chmod +x rsync.sh
	touch rsync.sh
