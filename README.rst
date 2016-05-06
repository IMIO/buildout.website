Introduction
============

This buildout relates the configuration of the application zope instance of the IMIO central server.

The main config file is buildout.cfg. But this file doesn't exists.
It's necessary to create a symlink to dev.cfg or prod.cfg.

The install process is described in the file : INSTALL.rst


Use minisite localy / dev
-------------------------

For using minisite for development you have to :

1. Make symlink between dev.cfg and buildout.cfg

    ln -fs dev.cfg buildout.cfg

2. Uncomment parts nginx and proxy

3. Install libpcre3 libpcre3-dev

    sudo apt-get install libpcre3 libpcre3-dev

4. Start buildout

    ./bin/buildout.cfg

5. Create minisite config file in var/instanace/minisites folder

Example : var/instance/minisites/ms.ini

    [/liege/fr/loisirs/culture/musees/la-boverie]
    minisite_url=http://127.0.0.2:8000
    portal_url=http://127.0.0.1:8000

    [/liege/en/leisure/culture/museums/la-boverie]
    minisite_url=http://127.0.0.3:8000
    portal_url=http://127.0.0.1:8000
