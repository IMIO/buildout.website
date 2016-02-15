# -*- coding: utf-8 -*-
from AccessControl.SecurityManagement import newSecurityManager
from Products.CMFCore.utils import getToolByName
from Testing import makerequest
from zope.component.hooks import setSite
from zope.globalrequest import setRequest
import logging
import transaction

logger = logging.getLogger('migrate plonesite')


def main(app):
    acl_users = app.acl_users
    user = acl_users.getUser('admin')
    if user:
        user = user.__of__(acl_users)
        newSecurityManager(None, user)
        logger.info("Retrieved the admin user")
    app = makerequest.makerequest(app)
    # support plone.subrequest
    app.REQUEST['PARENTS'] = [app]
    setRequest(app.REQUEST)
    container = app.unrestrictedTraverse('/')
    portal = get_plone_site(container)
    setSite(portal)
    portal_setup = getToolByName(portal, 'portal_setup')
    logger.info('---------- Start cpksin MIGRATION profile ----------')
    portal_setup.runAllImportStepsFromProfile('profile-cpskin.migration:migratetodx')
    transaction.commit()


def get_plone_site(container):
    result = ''
    for obj in container.values():
        if obj.meta_type == "Folder":
            for plone in obj.values():
                if plone.meta_type == "Plone Site":
                    result = plone
        else:
            if obj.meta_type == "Plone Site" and not result:
                result = obj
    return result

if __name__ == '__main__':
    main(app)
