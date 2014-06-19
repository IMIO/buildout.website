#!/usr/bin/make
#
all: run

.PHONY: bootstrap
bootstrap:
	virtualenv-2.7 --no-site-packages .
	if ! test -f buildout.cfg;then ln -s prod.cfg buildout.cfg;fi
	./bin/python bootstrap.py

.PHONY: buildout
buildout:
	if ! test -f bin/buildout;then make bootstrap;fi
	if ! test -f var/filestorage/Data.fs;then make standard-config; else bin/buildout -v;fi

.PHONY: dev-install
dev-install:
	if ! test -f buildout.cfg;then ln -s dev.cfg buildout.cfg;fi
	make buildout

.PHONY: standard-config
standard-config:
	if ! test -f bin/buildout;then make bootstrap;fi
	bin/buildout -v -c standard-config.cfg

.PHONY: run
run:
	if ! test -f bin/instance1;then make buildout;fi
	bin/instance1 fg

.PHONY: cleanall
cleanall:
	rm -fr develop-eggs downloads eggs parts .installed.cfg lib include bin buildout.cfg
