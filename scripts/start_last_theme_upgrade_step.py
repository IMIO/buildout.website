# -*- coding: utf-8 -*-
from AccessControl.SecurityManagement import newSecurityManager
from Acquisition import aq_get
# from AccessControl.SpecialUsers import system as user
from Products.CMFPlone.interfaces.siteroot import IPloneSiteRoot
from Testing import makerequest
from Zope2 import configure
from zope.component.hooks import setSite
from zope.globalrequest import setRequest

import argparse
import logging
import os
import sys
import transaction
import Zope2
logger = logging.getLogger('cpskin')


def get_site(zopeapp=None):
    zopeapp = makerequest.makerequest(app)  # noqa
    zopeapp.REQUEST['PARENTS'] = [app]  # noqa
    setRequest(zopeapp.REQUEST)
    # newSecurityManager(None, user)
    user = app.acl_users.getUser('admin')  # noqa
    newSecurityManager(None, user.__of__(app.acl_users)) # noqa
    portal = None
    for oid in app.objectIds():  # noqa
        obj = app[oid] # noqa
        if IPloneSiteRoot.providedBy(obj):
            portal = obj
    if not portal:
        raise('Do not find portal')
    setSite(portal)
    return portal


def get_themes(portal):
    themes = []
    ps = portal.portal_setup
    qi = portal.portal_quickinstaller
    quick_installed = [p['id'] for p in qi.listInstalledProducts()]
    all_profiles = [p['id'] for p in ps.listContextInfos()
                    if p['type'] == 'extension']
    cpskin_profiles = [p for p in all_profiles
                       if p.startswith('profile-cpskin.diazotheme.')]
    for profile_id in cpskin_profiles:
        if 'uninstall' in profile_id:
            continue
        if ps.getLastVersionForProfile(profile_id) == 'unknown':
            # profile is not installed
            logger.info('{0} is not installed - skipping'.format(profile_id))
            continue
        package_id = profile_id.split('-')[1].split(':')[0]
        if package_id in quick_installed:
            # profile is installed, product is also installed in quickinstaller
            themes.append(profile_id)
            logger.info('{0} is well installed - skipping'.format(profile_id))
    return themes


def start_last_upgrade_step(portal, themes):
    ps = portal.portal_setup
    for theme in themes:
        upgrades = ps.listUpgrades(theme, True)
        upgrade = sorted(upgrades, key=lambda k: k['sdest'])[-1]
        step = upgrade.get('step')
        logger.warn('Start last upgrade step for {0}'.format(theme))
        step.doStep(ps)


if __name__ == '__main__':
    portal = get_site(app)  # noqa
    themes = get_themes(portal)
    start_last_upgrade_step(portal, themes)
