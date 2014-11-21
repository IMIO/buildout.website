# -*- coding: utf-8 -*-
import logging
from zope.globalrequest import setRequest
from Testing import makerequest
from Products.CMFCore.utils import getToolByName
logger = logging.getLogger('create.plonesite')


def main(app):
    app = makerequest.makerequest(app)
    # support plone.subrequest
    app.REQUEST['PARENTS'] = [app]
    setRequest(app.REQUEST)
    container = app.unrestrictedTraverse('/')
    portal = get_plone_site(container)
    setup_tool = getToolByName(portal, 'portal_setup')
    setup_tool.runAllImportStepsFromProfile('profile-cpskin.migration:default')
    setup_tool.runAllImportStepsFromProfile('profile-collective.directory:migration')


def get_plone_site(container):
    for obj in container.values():
        if obj.meta_type == "Folder":
            for plone in obj.values():
                if plone.meta_type == "Plone Site":
                    result = plone
        elif obj.meta_type == "Plone Site":
            result = obj
    return result


if __name__ == '__main__':
    main(app)
