# -*- coding: utf-8 -*-
# ex : https://api.github.com/repos/imio/cpskin.core/tags
# ex :https://api.github.com/repos/imio/cpskin.core/commits

# command line : python get_releases_from_github jj/mm/aaaa login pwd
# To dev : Ask github api with token instead of login/pwd.
# Commit date format = u'date': u'2020-04-17T13:39:52Z'
import json
import requests
import sys
import urllib
import urlparse

from datetime import datetime

last_release_date = datetime.strptime(sys.argv[1], "%d/%m/%Y")
login = sys.argv[2]
pwd = sys.argv[3]

lst_products = [
    {
        "remote": "imio",
        "label": "plone.app.stagingbehavior",
        "check_tags": False
    },
    {
        "remote": "imio",
        "label": "collective.directory",
        "check_tags": True
    },
    {
        "remote": "imio",
        "label": "collective.faceted.taxonomywidget",
        "check_tags": False,
    },
    {
        "remote": "imio",
        "label": "collective.schedulefield",
        "check_tags": False
    },
    {
        "remote": "imio",
        "label": "collective.captchacontactinfo",
        "check_tags": True,
        "branch": "1.x"
    },
    {
        "remote": "imio",
        "label": "collective.printrss",
        "check_tags": True
    },
    {
        "remote": "imio",
        "label": "collective.sticky",
        "check_tags": False
    },
    {
        "remote": "imio",
        "label": "cpskin.cirkwi",
        "check_tags": True
    },
    {
        "remote": "imio",
        "label": "cpskin.caching",
        "check_tags": True
    },
    {
        "remote": "imio",
        "label": "cpskin.contenttypes",
        "check_tags": True
    },
    {
        "remote": "imio",
        "label": "cpskin.core",
        "check_tags": True
    },
    {
        "remote": "imio",
        "label": "cpskin.demo",
        "check_tags": True
    },
    {
        "remote": "imio",
        "label": "cpskin.agenda",
        "check_tags": True
    },
    {
        "remote": "imio",
        "label": "cpskin.locales",
        "check_tags": True
    },
    {
        "remote": "imio",
        "label": "cpskin.menu",
        "check_tags": True
    },
    {
        "remote": "imio",
        "label": "cpskin.migration",
        "check_tags": True
    },
    {
        "remote": "imio",
        "label": "cpskin.minisite",
        "check_tags": True
    },
    {
        "remote": "imio",
        "label": "cpskin.policy",
        "check_tags": True
    },
    {
        "remote": "imio",
        "label": "cpskin.citizen",
        "check_tags": True
    },
    {
        "remote": "imio",
        "label": "cpskin.localfood",
        "check_tags": True
    },
    {
        "remote": "imio",
        "label": "collective.preventactions",
        "check_tags": True
    },
    {
        "remote": "imio",
        "label": "cpskin.slider",
        "check_tags": True
    },
    {
        "remote": "imio",
        "label": "cpskin.theme",
        "check_tags": True
    },
    {
        "remote": "imio",
        "label": "cpskin.diazotheme.classic",
        "check_tags": True
    },
    {
        "remote": "imio",
        "label": "cpskin.diazotheme.dream",
        "check_tags": True
    },
    {
        "remote": "imio",
        "label": "cpskin.diazotheme.dreambasic",
        "check_tags": True
    },
    {
        "remote": "imio",
        "label": "cpskin.diazotheme.dreamRightPortlet",
        "check_tags": True,
    },
    {
        "remote": "imio",
        "label": "cpskin.diazotheme.dreamRightPortletBasic",
        "check_tags": True,
    },
    {
        "remote": "imio",
        "label": "cpskin.diazotheme.newDream",
        "check_tags": True
    },
    {
        "remote": "imio",
        "label": "cpskin.diazotheme.memory",
        "check_tags": True
    },
    {
        "remote": "imio",
        "label": "cpskin.diazotheme.modern",
        "check_tags": True
    },
    {
        "remote": "imio",
        "label": "cpskin.diazotheme.retro",
        "check_tags": True
    },
    {
        "remote": "imio",
        "label": "cpskin.diazotheme.slab",
        "check_tags": True
    },
    {
        "remote": "imio",
        "label": "cpskin.diazotheme.smart",
        "check_tags": True
    },
    {
        "remote": "imio",
        "label": "cpskin.diazotheme.spirit",
        "check_tags": True
    },
    {
        "remote": "imio",
        "label": "cpskin.diazotheme.trendy",
        "check_tags": True
    },
    {
        "remote": "imio",
        "label": "cpskin.diazotheme.trendybasic",
        "check_tags": True,
    },
    {
        "remote": "imio",
        "label": "cpskin.diazotheme.vicinity",
        "check_tags": True
    },
    {
        "remote": "imio",
        "label": "cpskin.workflow",
        "check_tags": True
    },
    {
        "remote": "imio",
        "label": "diazotheme.frameworks",
        "check_tags": True
    },
    {
        "remote": "4teamwork",
        "label": "ftw.blueprints",
        "check_tags": False
    },
    {
        "remote": "imio",
        "label": "imio.ATContentTypes.link",
        "check_tags": False
    },
    {
        "remote": "imio",
        "label": "imio.behavior.teleservices",
        "check_tags": False
    },
    {
        "remote": "imio",
        "label": "imio.ckeditortemplates",
        "check_tags": False
    },
    {
        "remote": "imio",
        "label": "imio.helpers",
        "check_tags": False
    },
    {
        "remote": "imio",
        "label": "imio.dashboard",
        "check_tags": False
    },
    {
        "remote": "imio",
        "label": "imio.media",
        "check_tags": False
    },
    {
        "remote": "imio",
        "label": "imio.gdpr",
        "check_tags": True
    },
    {
        "remote": "imio",
        "label": "imio.transmogrifier.blueprints",
        "check_tags": False,
    },
    {
        "remote": "imio",
        "label": "imio.transmogrifier.cardimporter",
        "check_tags": False,
    },
    {
        "remote": "imio",
        "label": "imio.transmogrifier.PloneFormGen",
        "check_tags": False,
    },
    {
        "remote": "imio",
        "label": "Products.CPUtils",
        "check_tags": False
    },
    {
        "remote": "imio",
        "label": "Products.directory",
        "check_tags": False
    },
    {
        "remote": "imio",
        "label": "collective.jsonmigrator",
        "check_tags": False
    },
    {
        "remote": "imio",
        "label": "pas.plugins.imio",
        "check_tags": False
    },
    {
        "remote": "redturtle",
        "label": "collective.limitfilesizepanel",
        "check_tags": False,
    },
    {
        "remote": "imio",
        "label": "pas.plugins.authomatic",
        "check_tags": False
    },
    {
        "remote": "imio",
        "label": "Products.PloneGazette",
        "check_tags": False
    },
    {
        "remote": "affinitic",
        "label": "affinitic.caching",
        "check_tags": False
    },
    {
        "remote": "imio",
        "label": "archetypes.multilingual",
        "check_tags": False
    },
    {
        "remote": "imio",
        "label": "collective.behavior.richdescription",
        "check_tags": False,
    },
    {
        "remote": "collective",
        "label": "collective.atomrss",
        "check_tags": False
    },
    {
        "remote": "collective",
        "label": "collective.ckeditor",
        "check_tags": False
    },
    {
        "remote": "collective",
        "label": "collective.ckeditortemplates",
        "check_tags": False,
    },
    {
        "remote": "collective",
        "label": "collective.compoundcriterion",
        "check_tags": False,
    },
    {
        "remote": "collective",
        "label": "collective.contact.core",
        "check_tags": True,
    },
    {
        "remote": "imio",
        "label": "collective.contact.importexport",
        "check_tags": False,
    },
    {
        "remote": "collective",
        "label": "collective.anysurfer",
        "check_tags": False,
    },
    {
        "remote": "collective",
        "label": "collective.documentgenerator",
        "check_tags": False,
    },
    {
        "remote": "collective",
        "label": "collective.eeafaceted.collectionwidget",
        "check_tags": False,
    },
    {
        "remote": "collective",
        "label": "collective.excelexport",
        "check_tags": False,
    },
    {
        "remote": "collective",
        "label": "collective.geo.behaviour",
        "check_tags": False,
    },
    {
        "remote": "collective",
        "label": "collective.geo.contentlocations",
        "check_tags": False,
    },
    {
        "remote": "collective",
        "label": "collective.geo.faceted",
        "check_tags": False,
    },
    {
        "remote": "collective",
        "label": "collective.geo.geographer",
        "check_tags": False,
    },
    {
        "remote": "collective",
        "label": "collective.geo.json",
        "check_tags": False
    },
    {
        "remote": "collective",
        "label": "collective.geo.leaflet",
        "check_tags": False,
    },
    {
        "remote": "collective",
        "label": "collective.js.leaflet",
        "check_tags": False
    },
    {
        "remote": "collective",
        "label": "collective.geo.mapwidget",
        "check_tags": False,
    },
    {
        "remote": "collective",
        "label": "collective.jekyll",
        "check_tags": False
    },
    {
        "remote": "collective",
        "label": "collective.lesscss",
        "check_tags": False
    },
    {
        "remote": "collective",
        "label": "collective.messagesviewlet",
        "check_tags": False,
    },
    {
        "remote": "collective",
        "label": "collective.monitor",
        "check_tags": False
    },
    {
        "remote": "collective",
        "label": "collective.plonefinder",
        "check_tags": False,
    },
    {
        "remote": "collective",
        "label": "collective.plonetruegallery",
        "check_tags": False,
    },
    {
        "remote": "collective",
        "label": "collective.quickupload",
        "check_tags": False,
    },
    {
        "remote": "collective",
        "label": "collective.recipe.buildoutcache",
        "check_tags": False,
    },
    {
        "remote": "collective",
        "label": "collective.taxonomy",
        "check_tags": False
    },
    {
        "remote": "collective",
        "label": "collective.transmogrifier",
        "check_tags": False,
    },
    {
        "remote": "collective",
        "label": "collective.upgrade",
        "check_tags": False
    },
    {
        "remote": "collective",
        "label": "wildcard.fixpersistentutilities",
        "check_tags": False,
    },
    {
        "remote": "collective",
        "label": "collective.z3cform.select2",
        "check_tags": False,
    },
    {
        "remote": "collective",
        "label": "eea.facetednavigation",
        "check_tags": False
    },
    {
        "remote": "collective",
        "label": "transmogrify.dexterity",
        "check_tags": False,
    },
    {
        "remote": "imio",
        "label": "communesplone.iconified_document_actions",
        "check_tags": False,
    },
    {
        "remote": "collective",
        "label": "wildcard.foldercontents",
        "check_tags": False,
    },
    {
        "remote": "collective",
        "label": "ploneorg.migration",
        "check_tags": False
    },
    {
        "remote": "collective",
        "label": "sc.social.like",
        "check_tags": False
    },
    {
        "remote": "plone",
        "label": "plone.app.linkintegrity",
        "check_tags": False
    },
    {
        "remote": "plone",
        "label": "plone.app.contenttypes",
        "check_tags": False
    },
    {
        "remote": "plone",
        "label": "plone.app.event",
        "check_tags": False
    },
    {
        "remote": "plone",
        "label": "plone.app.multilingual",
        "check_tags": False
    },
    {
        "remote": "plone",
        "label": "plone.app.collection",
        "check_tags": False
    },
    {
        "remote": "plone",
        "label": "plone.app.querystring",
        "check_tags": False
    },
    {
        "remote": "plone",
        "label": "plone.app.theming",
        "check_tags": False
    },
    {
        "remote": "zopefoundation",
        "label": "Products.ZNagios",
        "check_tags": False
    },
    {
        "remote": "collective",
        "label": "Solgema.fullcalendar",
        "check_tags": False
    },
    {
        "remote": "plone",
        "label": "plone.formwidget.querystring",
        "check_tags": False,
    },
    {
        "remote": "plone",
        "label": "plone.protect",
        "check_tags": False
    },
    {
        "remote": "plone",
        "label": "plone.outputfilters",
        "check_tags": False
    },
    {
        "remote": "plone",
        "label": "plone.app.textfield",
        "check_tags": False
    },
    {
        "remote": "plone",
        "label": "plone.i18n",
        "check_tags": False
    },
]

for product in lst_products:
    # ??
    if "captcha" in product.get("label"):
        continue
    github_commits_url = "https://api.github.com/repos/{}/{}/commits{}".format(
        product.get("remote"), product.get("label"), "?sha={}".format(
            product.get("branch")) if product.has_key("branch") else "")
    github_tags_url = "https://api.github.com/repos/{}/{}/tags".format(
        product.get("remote"), product.get("label"))
    github_url = "https://github.com/{}/{}".format(product.get("remote"),
                                                   product.get("label"))
    commits = requests.get(github_commits_url, auth=(login, pwd))
    try:
        last_commit_date_str = str(
            commits.json()[0].get("commit").get("committer").get("date")
        )
        last_commit_date = datetime.strptime(
            last_commit_date_str, "%Y-%m-%dT%H:%M:%SZ"
        )
        last_commit_committer_name = (
            commits.json()[0]
            .get("commit")
            .get("committer")
            .get("name")
            .encode("utf-8")
        )
    except Exception as e:
        print(e)
    if last_commit_date > last_release_date:
        if product.get("check_tags") is True:
            tags = requests.get(github_tags_url, auth=(login, pwd))
            try:
                dic = json.loads(tags.content)
                last_tag = dic[0].get("name")
            except Exception as e:
                print(e)
        else:
            last_tag = ""

        msg = (
            "{} : PAR {} EN DATE DU {} ({}). Tags en ligne : {} | Tags versions-base : {}"
        ).format(product.get("label"), last_commit_committer_name,
                 last_commit_date_str, github_url, last_tag, "0.00")
        print(msg)
