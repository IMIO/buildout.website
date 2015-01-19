# -*- coding: utf-8 -*-
import logging
from zope.globalrequest import setRequest
from Testing import makerequest
from Products.CMFCore.utils import getToolByName
from AccessControl.SecurityManagement import newSecurityManager
from zope.component.hooks import setSite
logger = logging.getLogger('migrate plonesite')
import transaction


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
    logger.info('---------- Start direcotry MIGRATION profile ----------')
    portal_setup.runAllImportStepsFromProfile('profile-collective.directory:migration')
    logger.info('---------- Start cpksin MIGRATION profile ----------')
    portal_setup.runAllImportStepsFromProfile('profile-cpskin.migration:default')
    logger.info('---------- Detele old Products.directory ----------')
    portal_setup.runAllImportStepsFromProfile('profile-Products.directory:uninstall')

    # install cputils
    if not hasattr(app, 'cputils_install'):
        from Products.ExternalMethod.ExternalMethod import manage_addExternalMethod
        manage_addExternalMethod(app, 'cputils_install', '', 'CPUtils.utils', 'install')
        app.cputils_install(app)
        logger.info("Cpskin installed")

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
