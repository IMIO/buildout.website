#!/usr/bin/env python
# -*- coding: utf-8 -*-
from AccessControl.SecurityManagement import newSecurityManager
from AccessControl.SecurityManagement import noSecurityManager
from collective.transmogrifier.transmogrifier import Transmogrifier
from cpskin.migration.blueprints.utils import BATCH_CURRENT_KEY
from cpskin.migration.blueprints.utils import BATCH_SIZE_KEY
from cpskin.migration.blueprints.utils import CURRENT_KEY
from cpskin.migration.blueprints.utils import TOTAL_OBJECTS_KEY
from Products.CMFPlone.interfaces.siteroot import IPloneSiteRoot
from Testing import makerequest
from zope.annotation.interfaces import IAnnotations
from zope.component.hooks import setSite
from zope.globalrequest import setRequest

import logging
import sys
import transaction


logger = logging.getLogger('cpskin-dx-transmo')
logger.setLevel(logging.INFO)
ch = logging.StreamHandler(sys.stdout)
ch.setLevel(logging.INFO)
formatter = logging.Formatter('%(asctime)s %(levelname)s %(name)s %(message)s',
                              '%Y-%m-%d %H:%M:%S')
ch.setFormatter(formatter)
logger.addHandler(ch)


def get_portal(zopeapp=None):
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
    setSite(portal)
    return portal


def main(app):
    """
    desactivate and save (in dtml doc) authentication plugin
    """
    app = makerequest.makerequest(app)
    # support plone.subrequest
    app.REQUEST['PARENTS'] = [app]
    setRequest(app.REQUEST)
    # container = app.unrestrictedTraverse('/')
    acl_users = app.acl_users
    user = acl_users.getUser('admin')
    if user:
        user = user.__of__(acl_users)
        newSecurityManager(None, user)
        logger.info('Retrieved the admin user')
    portal = get_portal(app)

    config = 'cpskin.blueprints.dexterity'
    transmogrifier = Transmogrifier(portal)
    anno = IAnnotations(portal)
    if BATCH_CURRENT_KEY not in anno.keys():
        batch_current = 0
        anno[BATCH_CURRENT_KEY] = 0
    else:
        batch_current = anno[BATCH_CURRENT_KEY]
    batch_size = 750
    anno[BATCH_SIZE_KEY] = batch_size

    # transmogrifier.context = portal
    # for i in range(total_objects / batch_size):
    output = transmogrifier(config)  # noqa
    transaction.commit()
    noSecurityManager()
    total_objects = anno[TOTAL_OBJECTS_KEY]
    batch_current = anno[BATCH_CURRENT_KEY]
    logger.info('End of batch: {0} / {1}'.format(batch_current, total_objects))

    if total_objects > batch_current:
        # not finished
        return 0
    else:
        # delete annotations
        del anno[BATCH_SIZE_KEY]
        del anno[BATCH_CURRENT_KEY]
        del anno[TOTAL_OBJECTS_KEY]
        del anno[CURRENT_KEY]
        return 1


if __name__ == '__main__':
    ret = main(app)  # noqa
    sys.exit(ret)
