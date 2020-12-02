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


Migrate one package
-------------------

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
- Manu-iMio
- mpeeters
- nballeux
- tlambert


Packages already migrated
-------------------------

- collective.contact.importexport
- collective.directory
- collective.faceted.taxonomywidget
- collective.preventactions
- collective.printrss
- collective.schedulefield
- collective.sticky
- cpskin.agenda
- cpksin.caching
- cpskin.cirkwi
- cpskin.citizen
- cpskin.core
- cpskin.contenttypes
- cpskin.demo
- cpskin.diazotheme.classic
- cpskin.diazotheme.dream
- cpskin.diazotheme.dreambasic
- cpskin.diazotheme.dreamRightPortlet
- cpskin.diazotheme.dreamRightPortletBasic
- cpskin.diazotheme.memory
- cpskin.diazotheme.modern
- cpskin.diazotheme.retro
- cpskin.diazotheme.smart
- cpskin.diazotheme.spirit
- cpskin.diazotheme.trendy
- cpskin.diazotheme.trendybasic
- cpskin.diazotheme.vicinity
- cpskin.locales
- cpskin.localfood
- cpskin.menu
- cpskin.minisite
- cpskin.policy
- cpskin.slider
- cpskin.theme
- cpskin.workflow
- imio.behavior.teleservices
- imio.ckeditortemplates
- imio.gdpr
- imio.media
- plone.app.stagingbehavior : Problem with version (+imio1)
