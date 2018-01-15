# -*- coding: utf-8 -*-
from AccessControl.SecurityManagement import newSecurityManager
from plone.dexterity.utils import safe_utf8
from Products.CMFPlone.interfaces.siteroot import IPloneSiteRoot
from Products.PloneFormGen.interfaces.field import IPloneFormGenField
from Testing import makerequest
from zope.component.hooks import setSite
from zope.globalrequest import setRequest

import logging
import sys
import transaction


logger = logging.getLogger('cpskin-unicode-errors')
logger.setLevel(logging.INFO)
ch = logging.StreamHandler(sys.stdout)
ch.setLevel(logging.INFO)
formatter = logging.Formatter('%(asctime)s %(levelname)s %(name)s %(message)s',
                              '%Y-%m-%d %H:%M:%S')
ch.setFormatter(formatter)
logger.addHandler(ch)


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


def get_pfg_contents(portal):
    pfg_contents = []
    portal_catalog = portal.portal_catalog
    query = {}
    query['object_provides'] = IPloneFormGenField.__identifier__
    brains = portal_catalog(query)
    for brain in brains:
        pfg_contents.append(brain.getObject())
    return pfg_contents


def correct_archetypes(objects):
    for obj in objects:
        desc = safe_utf8(obj.Description())
        obj.setDescription(desc)
        obj.description = desc
        obj.reindexObject()
        obj.processForm()
        transaction.commit()
        logger.info('{0} updated'.format(obj.absolute_url()))


if __name__ == '__main__':
    portal = get_site(app)  # noqa
    objects = get_pfg_contents(portal)
    correct_archetypes(objects)
