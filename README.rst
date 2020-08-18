Introduction
------------

This buildout assemble all related configuration of the application zope instance of the iMio iA.Smartweb app.

.. contents:: Table of contents

Update cpskin
-------------
Make new release of a single package
====================================

To make release of a package:

- Configure your .pypirc file (see iMio internal documentation)
- Install zest.releaser

After that, you can make a release with zest.releaser

**But first check if you have already update changelog (usually on CHANGES.rst file).**

Update version of your package
==============================

Go to buildout-website (https://github.com/IMIO/buildout.website) and in versions-base.cfg file, change version of package you just release.

Data
--------
make rsync will data. You can add blobs or data args (b for blobstorage, d for Data.fs)::

    make rsync d

Dev
---
Start developping::

  make dev

and start instance::

  ./bin/instance fg

Dev with docker
---------------
First you have to install docker and docker-compose

After that, you have to build local image and up container::

    make build
    make up

or you can build and go to container, add some pdb and start instance like this::

    make build
    make bash
    # *change what you want*
    bin/instance-debug fg

.env file
----------
.env file is used to get some information about project you are working on

list of keys :
    - uid
    - projectid
    - servername
    - minisites

example ::

    uid=1000
    projectid=liege
    servername=staging.lan.imio.be
    minisites=['/fr/decouvrir/culture/musees/la-boverie']

You can generate .env file with `make env` command

Minisites
---------
::

  make minisites

Create minisites ini files (in var/instance/minisites folder) and generate traefik.toml file
You can see minisite urls on http://portal.localhost/minisites_panel when instance is up.

Monitoring
----------
You can monitor your instance with these command::

  echo 'uptime' | nc -i 1 localhost 8888
  echo 'stats' | nc -i 1 localhost 8888

Or connect to port 8888 with telnet

All available monitoring command can get with this command::

  echo 'help' | nc -i 1 localhost 8888
