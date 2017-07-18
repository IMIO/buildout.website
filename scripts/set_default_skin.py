# -*- coding: utf-8 -*-
from AccessControl.SecurityManagement import newSecurityManager
from Acquisition import aq_get
# from AccessControl.SpecialUsers import system as user
from Products.CMFPlone.interfaces.siteroot import IPloneSiteRoot
from Testing import makerequest
from Zope2 import configure
from zope.globalrequest import setRequest

import argparse
import logging
import os
import sys
import transaction
import Zope2


logger = logging.getLogger('cpskin')
# parser = argparse.ArgumentParser(description='Run a script')
# parser.add_argument('--plone-path', dest='plone_path',
#                     help='Set plone path (example: Plone)')
# parser.add_argument('-c')  # use to bin/instance run script.py


def get_site(zopeapp=None):
    # if 'PROJECT_ID' in os.environ:
    #     plone_path = os.environ['PROJECT_ID']
    #     conf_path = '/home/imio/imio-website/parts/instance/etc/zope.conf'
    # else:
    #     args = parser.parse_args()
    #     plone_path = args.plone_path
    #     conf_path = 'parts/instance/etc/zope.conf'
    # if not plone_path:
    #     return
    # if not zopeapp:
    #     configure(conf_path)
    #     zopeapp = Zope2.app()
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
        raise('Do not find poratl')
    return portal


def set_default_skin(argv=sys.argv):
    portal = get_site(argv)
    portal_skins = portal.get('portal_skins')
    selected_skin = 'Sunburst Theme'
    if portal_skins.default_skin != selected_skin:
        portal_skins.default_skin = selected_skin
        request = aq_get(portal, 'REQUEST', None)
        portal.changeSkin(selected_skin, request)
        transaction.commit()
        logger.info('Restored default_skin : {0}'.format(selected_skin))


if __name__ == '__main__':
    set_default_skin(app) # noqa
