#!/usr/bin/make
#
all: run
VERSION=`cat version.txt`
#BUILD_NUMBER := debug1

bootstrap.py:
	wget http://downloads.buildout.org/2/bootstrap.py

buildout.cfg:
	ln -fs dev.cfg buildout.cfg
	#ln -fs prod.cfg buildout.cfg

bin/python:
	virtualenv-2.7 --no-site-packages .

bin/buildout: bin/python buildout.cfg bootstrap.py
	./bin/pip install zc.buildout

.PHONY: buildout
buildout: bin/buildout
	bin/buildout -t 7

.PHONY: standard-config
standard-config: bin/buildout
	bin/buildout -c standard-config.cfg

.PHONY: robot-server
robot-server:
	bin/robot-server -v cpskin.policy.testing.CPSKIN_POLICY_ROBOT_TESTING

.PHONY: run
run: buildout
	bin/instance fg

.PHONY: cleanall
cleanall:
	rm -fr develop-eggs downloads eggs parts .installed.cfg lib include bin .mr.developer.cfg

.PHONY: deb
deb:
	git-dch -a --ignore-branch
	dch -v $(VERSION).$(BUILD_NUMBER) release --no-auto-nmu
	dpkg-buildpackage -b -uc -us

.PHONY: mrbob
mrbob: bin/python
	./bin/easy_install -i http://pypi.imio.be/imio/imio/+simple/ bobtemplates.imio
	echo "[variables]" > debian.ini
	echo "debian.name = mutual" >> debian.ini
	./bin/mrbob -c debian.ini -O debian bobtemplates:debian

.PHONY: migration
migration: bootstrap.py bin/python
	ln -fs migration.cfg buildout.cfg
	bin/buildout -t 7
	bin/rsync-datafs
	bin/rsync-blobstorage
	bin/instance-migration run migration.py
	bin/instance fg

.PHONY: migration-dev
migration-dev: bootstrap.py bin/python
	ln -fs migration2dx-dev.cfg buildout.cfg
	bin/buildout -t 7
	bin/rsync-datafs
	bin/rsync-blobstorage
	bin/instance-migration fg

docker-image:
	docker build -t plone-imio-website:latest .

docker-migration-image:
	docker build -f Dockerfile.migration -t website-migration:latest .

docker-cleanup-image:
	docker build -f Dockerfile.cleanup -t website-cleanup:latest .

docker-transmo-image:
	docker build -f Dockerfile.transmo -t website-transmo:latest .

docker-migration-transmo-image:
	docker build -f Dockerfile.migrationtransmo -t website-migration-transmo:latest .

buildout-cache: bootstrap.py bin/python bin/buildout
	mkdir -p buildout-cache/downloadst
	./bin/buildout -t 25 -c docker.cfg install makebuildoutcache
	mkdir -p tmp/buildout-cache/downloads/dist/
	wget http://devpi.imio.be/root/pypi/+f/b73/445dc0069550b/geopy-1.11.0.tar.gz -O tmp/buildout-cache/downloads/dist/geopy-1.11.0.tar.gz
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

buildout-docker-dev:
	bin/buildout -c docker.cfg buildout:eggs-directory=~/.buildout/eggs buildout:download-cache=~/.buildout/download-cache

zeoserver-docker-start:
	echo "bushy" > var/blobstorage/.layout
	bin/zeoserver start

instance-docker-fg: zeoserver-docker-start
	HOSTNAME_HOST=localhost ZEO_HOST=localhost ZEO_PORT=8100 PROJECT_ID=dev ./bin/instance fg instance:shared-blob=on

buildout-migration-docker: buildout-cache/downloads
	bin/buildout -t 22 -c migration2dx.cfg

buildout-transmo-docker: buildout-cache/downloads
	bin/buildout -t 22 -c transmo-prod.cfg

buildout-migration-transmo-docker: buildout-cache/downloads
	bin/buildout -t 22 -c transmo.cfg eggs-directory=buildout-cache/eggs download-cache=buildout-cache/downloads

buildout-cleanup-docker: buildout-cache/downloads
	bin/buildout -t 22 -c migration.cfg
