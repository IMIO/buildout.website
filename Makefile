#!/usr/bin/make
#
all: run

.PHONY: bootstrap
bootstrap:
	virtualenv-2.6 --no-site-packages .
	./bin/python bootstrap.py
	./bin/subproducts.sh

.PHONY: buildout
buildout:
	if ! test -f bin/buildout;then make bootstrap;fi
	bin/buildout -v

.PHONY: run
run:
	if ! test -f bin/instance;then make buildout;fi
	bin/instance fg

.PHONY: cleanall
cleanall:
	rm -fr develop-eggs downloads eggs parts .installed.cfg

.PHONY: libraries
libraries: 
	./bin/subproducts.sh
