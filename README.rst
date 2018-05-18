Introduction
------------

This buildout relates the configuration of the application zope instance of the IMIO central server.

The main config file is buildout.cfg. But this file doesn't exists.
It's necessary to create a symlink to dev.cfg or prod.cfg.

The install process is described in the file : INSTALL.rst


Update cpskin
-------------

To update cpskin, you have to make a new release of your package you would like to update and change version of this package on buildout.


Make new release of a single package
===================================

To make release of a package you of to use zest.releaser and you have to have you .pypirc update

Configure your .pypirc file :
http://www.imio.be/support/documentation/manual/release-locale-imio/uploader-nos-oeufs-sur-notre-serveur-doeufs


Then you have to install zest.releaser :
http://www.imio.be/support/documentation/how-to/publier-un-oeuf-egg-release-avec-zest.releaser

After that, you can make a release as explain in that link above.

**But first check if you have already update changelog (often CHANGES.rst file).**

Update version of your package
==============================

Go to buildout-website (https://github.com/IMIO/buildout.website) and in versions-base.cfg file, change version of package you just release.


Monitoring
----------
telnet 127.0.0.1 8888
stats

echo 'uptime' | nc -i 1 localhost 8888

Get Data
--------

make rsync will data. You can add blobs or data args (b for blobstorage, d for Data.fs)

    make rsync d

Dev with docker
---------------
First you have to install docker and docker-compose

After that, you have to build local image and up container::

    $ make build
    $ make up

Complete .env file
------------------
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
`make minisites` command create minisites ini files (in var/instance/minisites folder) and generate traefik.toml file

http://portal.localhost/minisites_panel
