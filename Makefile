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

bin/python:
	virtualenv-2.7 --no-site-packages .

bin/buildout: bin/python buildout.cfg
	./bin/pip install setuptools==33.1.1
	./bin/pip install zc.buildout==2.9.5

.PHONY: buildout
buildout: bin/buildout
	bin/buildout -t 7


.PHONY: robot-server
robot-server:
	bin/robot-server -v cpskin.policy.testing.CPSKIN_POLICY_ROBOT_TESTING

.PHONY: run
run: buildout
	bin/instance fg

.PHONY: cleanall
cleanall:
	rm -fr develop-eggs downloads eggs parts .installed.cfg lib include bin .mr.developer.cfg .env nginx.conf

docker-image:
	docker build -t plone-imio-website:latest .

docker-migration-transmo-image:
	docker build --no-cache -f Dockerfile.migrationtransmo -t website-migration-transmo:latest .
	docker tag website-migration-transmo:latest docker-staging.imio.be/website-migration-transmo:latest
	docker push docker-staging.imio.be/website-migration-transmo:latest

buildout-cache: bin/python bin/buildout
	mkdir -p buildout-cache/downloads
	./bin/buildout -t 25 -c docker.cfg install makebuildoutcache
	#mkdir -p tmp/buildout-cache/downloads/dist/
	#wget http://devpi.imio.be/root/pypi/+f/b73/445dc0069550b/geopy-1.11.0.tar.gz -O tmp/buildout-cache/downloads/dist/geopy-1.11.0.tar.gz
	./bin/makebuildoutcache
	rm -rf buildout-cache

buildout-cache/downloads:
	rm -rf buildout-cache
	wget -O buildout-cache.tar.bz2 http://files.imio.be/website-buildout-cache.tar.bz2
	tar jxvf buildout-cache.tar.bz2 1>/dev/null
	rm buildout-cache.tar.bz2

buildout-docker: buildout-cache/downloads
	# check if buildout-cache/download folder exists, if not, make get-buildout-cache
	#mkdir -p buildout-cache/downloads
	#bin/buildout -N -c prod.cfg install download
	bin/buildout -t 22 -c docker.cfg

buildout-migration-transmo-docker: buildout-cache/downloads
	bin/buildout -t 22 -c transmo-migrate-to-dx.cfg eggs-directory=buildout-cache/eggs download-cache=buildout-cache/downloads

var/instance/minisites:
	mkdir -p var/instance/minisites

minisites-conf:
	scripts/minisites-conf.py --projectid ${PROJECTID}

.env:
	echo uid=${UID} > .env
	echo projectid=${PROJECTID} >> .env

build:
	docker-compose pull
	docker-compose run zeo /usr/bin/python bootstrap.py -c docker-dev.cfg --buildout-version 2.7.0
	docker-compose run zeo bin/buildout -c docker-dev.cfg

up: .env var/instance/minisites
	docker-compose up
