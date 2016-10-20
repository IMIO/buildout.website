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


Use minisite localy / dev
-------------------------

For using minisite for development you have to :

1. Make symlink between dev.cfg and buildout.cfg
::
    ln -fs dev.cfg buildout.cfg

2. In dev.cfg: uncomment parts nginx and proxy, update path of minisite(s) (in 'proxy' section)
::

3. Install libpcre3 libpcre3-dev
::
    sudo apt-get install libpcre3 libpcre3-dev

4. Start buildout
::
    ./bin/buildout

5. Create minisite config file in var/instance/minisites folder
::

Example : var/instance/minisites/ms.ini
::
    [/liege/fr/loisirs/culture/musees/la-boverie]
    minisite_url=http://127.0.0.2:8000
    portal_url=http://127.0.0.1:8000

    [/liege/en/leisure/culture/museums/la-boverie]
    minisite_url=http://127.0.0.3:8000
    portal_url=http://127.0.0.1:8000

6. Start proxy
::
    ./bin/proxy start

7. Start instance
::
    ./bin/instance fg

You can now go to `http://127.0.0.1:8000` to see one minisite


Monitoring
----------
telnet 127.0.0.1 8888
stats

echo 'uptime' | nc -i 1 localhost 8888
