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

Using twine to upload to pypi : 

twine upload -r pypi dist/*



Account to add to packages:

- bsuttor
- cboulanger
- imio
- laz
- mpeeters
- Manu-iMio
- nballeux


Packages already migrated
-------------------------

- cpskin.core
- cpskin.citizen
