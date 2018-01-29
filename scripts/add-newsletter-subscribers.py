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
        spliter = len(os.environ['REMOTE_TRANSMO_URL'].split('/')) - 3
        newslettertheme_path = '/{0}'.format('/'.join(path.split('/')[spliter+1:]))  # noqa
        newslettertheme = api.content.get(newslettertheme_path)
        abonnes_folder = [x for x in newslettertheme.objectIds() if 'abonnes' in x]
        for abonnes_folder_id in abonnes_folder:
            abonne_folder = getattr(newslettertheme, abonnes_folder_id)
            if abonne_folder.portal_type == 'NewsletterBTree':
                newslettertheme.subscriber_folder_id = abonne_folder
                logger.info(
                    'Set subscriber_folder_id to {0}'.format(abonne_folder.id))
        tot = len(subscribers)
        i = 0
        for subscriber in subscribers:
            i += 1
            email = subscriber.get('email')
            active = subscriber.get('active')
            fullname = subscriber.get('fullname')
            form = subscriber.get('format')
            if not newslettertheme.alreadySubscriber(email):
                newId = newslettertheme._getRandomIdForSubscriber()
                newsubscriber = newslettertheme.createSubscriberObject(newId)
                newsubscriber.fullname = fullname
                newsubscriber.edit(
                    format=form,
                    active=active,
                    email=email
                )
                logger.info('{0}/{1} {2} added in {3}'.format(
                    i, tot, email, path)
                )
            else:
                logger.info('{0} already in {1}'.format(email, path))

        remote_url = os.environ['REMOTE_TRANSMO_URL']
        remote_username = os.environ['REMOTE_TRANSMO_USERNAME']
        remote_password = os.environ['REMOTE_TRANSMO_PASSWORD']
        url = '{0}{1}/get_item'.format(remote_url, path)
        req = requests.get(url,  auth=(remote_username, remote_password))
        results = req.json()
        newslettertheme.title = results.get('title', newslettertheme.id)
        ntfields = [
            'title',
            'description',
            'testEmail',
            'authorEmail',
            'replyto',
            'activationMailSubject',
            'activationMailTemplate',
            'newsletterHeader',
            'newsletterFooter',
            'newsletterStyle',
            'notify',
            'renderTemplate',
            'extraRecipients',
            'subscriber_folder_id',
            'alternative_portal_url',
        ]
        for ntfield in ntfields:
            if not getattr(newslettertheme, ntfield, None):
                setattr(newslettertheme, ntfield, results.get(ntfield))

        newslettertheme.reindexObject()

        children = get_children('{0}{1}'.format(remote_url, path))

        for child in children:
            logger.info('{0}/{1}'.format(path, child))
            children_item = get_item('{0}{1}/{2}'.format(remote_url, path, child))
            classname = children_item.get('_classname')
            if classname == 'Newsletter':
                newsletterid = children_item.get('_id')
                if newsletterid not in newslettertheme.objectIds():
                    newslettertheme.invokeFactory('Newsletter', newsletterid)
                newsletter = newslettertheme[newsletterid]
                # newsletter.text = children_item.get('text')
                # newsletter.title = children_item.get('title')
                newletterfields = [
                    'text',
                    'title',
                    'description',
                    'setFormat',
                    'dateEmitted'
                ]
                for newletterfield in newletterfields:
                    if not getattr(newsletter, newletterfield, None):
                        setattr(newsletter, newletterfield, children_item.get(newletterfield))
                newsletter.reindexObject()
                nl_children = get_children('{0}{1}/{2}'.format(remote_url, path, child))
                for nl_child in nl_children:
                    nl_child_item = get_item('{0}{1}/{2}/{3}'.format(remote_url, path, child, nl_child))
                    if nl_child_item.get('_classname') in ('NewsletterBTree', 'NewsletterReference'):
                        nl_child_id = nl_child_item.get('_id')
                        if nl_child_id not in newsletter.objectIds():
                            newsletter.invokeFactory(nl_child_item.get('_classname'), nl_child_id)
                            if nl_child.get('text'):
                                newsletter[nl_child_id].text = nl_child.get('text')

    logger.info('Commit transaction')
    transaction.commit()


def add_subscriber(newslettertheme, subscriber_item):
    email = subscriber_item.get('email')
    active = subscriber_item.get('active')
    fullname = subscriber_item.get('fullname')
    form = subscriber_item.get('format')
    if not newslettertheme.alreadySubscriber(email):
        newId = newslettertheme._getRandomIdForSubscriber()
        newsubscriber = newslettertheme.createSubscriberObject(newId)
        newsubscriber.fullname = fullname
        newsubscriber.edit(
            format=form,
            active=active,
            email=email
        )


def get_item(obj_url):
    remote_username = os.environ['REMOTE_TRANSMO_USERNAME']
    remote_password = os.environ['REMOTE_TRANSMO_PASSWORD']
    url = '{0}/get_item'.format(obj_url)
    req = requests.get(url,  auth=(remote_username, remote_password))
    try:
        results = req.json()
    except:
        results = {}
    return results


def get_children(obj_url):
    remote_username = os.environ['REMOTE_TRANSMO_USERNAME']
    remote_password = os.environ['REMOTE_TRANSMO_PASSWORD']
    url = '{0}/get_children'.format(obj_url)
    req = requests.get(url,  auth=(remote_username, remote_password))
    try:
        results = req.json()
    except:
        results = {}
    return results


if __name__ == '__main__':
    portal = get_site(app)  # noqa
    subscribers = get_subscribers()
    add_subscribers(portal, subscribers)
