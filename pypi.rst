Migrate to Pypi.org
===================

Before migration
----------------

1. Create an account on pypi
2. Add your account on your home linux user folder ~/.pypirc file
3. Remove old devpi part on your home linux user folder ~/.pypirc file

Your .pypirc file should looks like::

    [distutils]
    index-servers =
        pypi

    [pypi]
    username: bsuttor
    password: my-super-password


Migrate on package
------------------

1. Go to the package and co latest tag:
example::
    cd src/cpskin.core
    # see latest tags
    git describe --tags --abbrev=0
    # go to latest tag
    git checkout -b 1.1.3 tags/1.1.3
    # make a release
    release
    # and return to master branch
    git co master
    
2. Go to pypi.org and add user above as owner

Account to add to packages
--------------------------

- bsuttor
- cboulanger
- imio
- laz
- mpeeters
- Manu-iMio
- nballeux
- tlambert


Packages already migrated
-------------------------

- cpksin.caching
- cpskin.core
- cpskin.citizen
- cpskin.contenttypes
- cpskin.demo
