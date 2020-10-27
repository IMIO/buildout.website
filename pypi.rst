# Migrate to Pypi.org

## Before migration

1. Create an account on pypi
2. Add your account on your ~/.pypirc file
3. Remove old devpi part on ~/.pypirc file

Your .pypirc file should looks like::

    [distutils]
    index-servers =
        pypi

    [pypi]
    username: bsuttor
    password: my-super-password


## Migrate on package



Account to add to packages:
- bsuttor
- cboulanger
- imio
