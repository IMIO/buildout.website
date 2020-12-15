Introduction
------------
This buildout assemble all related configuration of the application zope instance of the iMio iA.Smartweb app.

.. contents:: Table of contents

Prerequisite
-------------
To make a release you need to:

- Install zest.releaser

After that, you can make a release with `zest.releaser <https://pypi.org/project/zest.releaser/>`_

Deploy on staging
-----------------
Each commit on this repository launch a new version of iA.Smartweb app on your staging instances.

If you want to avoid a new release, you have to add **[ci skip]** on your commit message.

To update a package:

- Update version of the package on versions-base.cfg
- Complete changelog on CHANGES.rst

Deploy on production
--------------------
A buildout release is used to deploy all changes on production. Before making a release, you need to check if:

- your repo is up to date (eg. use ``git pull`` command)
- changelog is filled (see CHANGES.rst file)

Release
=======
As explain in `Prerequisite`_ we use `zest.releaser <https://pypi.org/project/zest.releaser/>`_ so you just have to make:

    fullrelease

And that's all. Jenkins will deploy latest docker image on production and restart services next night.

Release a immediately
=====================
If you add *quick* on name of the release. Jenkins will restart all instances immediately.

Get data locally
----------------
You can get data from production instance on our local env with this command::

    make rsync

You can use blobs or data args (b for blobstorage, d for Data.fs)::

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
