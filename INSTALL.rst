Dependencies
============

We assume the installation in the folder /srv/zinstances/site433
 (that can be changed) and on an ubuntu distribution.
Your real username must replace in our commands the string "username".
Each command, specified by the symbol "$" or "#", can be executed 
 (without the symbol).

First we become root::
    
    $ sudo -s

We install the necessary libraries::

    # apt-get install build-essential
    # apt-get install libreadline6-dev
    # apt-get install zlib1g-dev (support zlib)
    # apt-get install libbz2-dev
    # apt-get install libjpeg62-dev
    # apt-get install subversion
    # apt-get install git
    # apt-get install libpq-dev
    # apt-get install libxml2-dev
    # apt-get install libxslt1-dev
    # apt-get install make
    # exit

Install Python
==============

If you don't have python installed, we have to install it with virtualenv


Install Buildout for dev
========================

We download the buildout files in our folder::

    $ git clone https://github.com/IMIO/buildout.website.git plone-imio

And go into buildout::

    $ cd plone-imio


After you can use make for buildout install::

    $ make run

You can now start the plone site::

    $ bin/instance1 fg
    OR
    $ bin/instance1 start

We can connect the zope server in a browser on the following address http://localhost:8080/manage_main
