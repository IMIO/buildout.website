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
	./bin/python bootstrap.py

.PHONY: buildout
buildout: bin/buildout
	bin/buildout -t 7

.PHONY: standard-config
standard-config: bin/buildout
	bin/buildout -c standard-config.cfg

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

docker-image:
	docker build -t plone-imio:latest .

buildout-cache: bootstrap.py bin/python
	mkdir -p buildout-cache/downloads
	./bin/python bootstrap.py -c docker.cfg
	./bin/buildout -t 15 -c docker.cfg install makebuildoutcache
	mkdir -p tmp/buildout-cache/downloads/dist/
	wget http://pypi.imio.be/root/pypi/+f/e2d/6e9ea7d8845bf/plone.app.multilingual-2.0.1.zip -O tmp/buildout-cache/downloads/dist/plone.app.multilingual.zip
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
	bin/buildout -t 15 -c docker.cfg
