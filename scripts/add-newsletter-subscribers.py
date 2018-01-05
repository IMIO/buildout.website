# -*- coding: utf-8 -*-
from AccessControl.SecurityManagement import newSecurityManager
from plone import api
from Products.CMFPlone.interfaces.siteroot import IPloneSiteRoot
from Testing import makerequest
from zope.component.hooks import setSite
from zope.globalrequest import setRequest

import logging
import os
import requests
import sys
import transaction


logger = logging.getLogger('cpskin-import-subscribers')
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


def get_subscribers():
    remote_url = os.environ['REMOTE_TRANSMO_URL']
    remote_username = os.environ['REMOTE_TRANSMO_USERNAME']
    remote_password = os.environ['REMOTE_TRANSMO_PASSWORD']
    url = '{0}/transmo-export'.format(remote_url)
    req = requests.get(url,  auth=(remote_username, remote_password))
    results = req.json()
    return results.get('newsletters', {})


def add_subscribers(portal, src_subscribers):
    for path, subscribers in src_subscribers.items():
        portal_path = '/'.join(portal.getPhysicalPath())
        newsletterttheme_path = path.replace(portal_path, '')
        newsletterttheme = api.content.get(newsletterttheme_path)
        tot = len(subscribers)
        i = 0
        for subscriber in subscribers:
            i += 1
            email = subscriber.get('email')
            active = subscriber.get('active')
            fullname = subscriber.get('fullname')
            form = subscriber.get('format')
            if not newsletterttheme.alreadySubscriber(email):
                newId = newsletterttheme._getRandomIdForSubscriber()
                newsubscriber = newsletterttheme.createSubscriberObject(newId)
                newsubscriber.fullname = fullname
                newsubscriber.edit(
                    format=form,
                    active=active,
                    email=email
                )
                logger.info('{0}/{1} {2} added in {3}'.format(
                    i, tot, email, path)
                )
                if i % 25 == 0:
                    logger.info('Commit transaction')
                    transaction.commit()
            else:
                logger.info('{0} already in {1}'.format(email, path))

        remote_url = os.environ['REMOTE_TRANSMO_URL']
        remote_username = os.environ['REMOTE_TRANSMO_USERNAME']
        remote_password = os.environ['REMOTE_TRANSMO_PASSWORD']
        url = '{0}{1}/get_item'.format(remote_url, path)
        req = requests.get(url,  auth=(remote_username, remote_password))
        results = req.json()
        newsletterttheme.title = results.get('title', newsletterttheme.id)
        newsletterttheme.reindexObject()
    transaction.commit()


if __name__ == '__main__':
    portal = get_site(app)  # noqa
    subscribers = get_subscribers()
    add_subscribers(portal, subscribers)
