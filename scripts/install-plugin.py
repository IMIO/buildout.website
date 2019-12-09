# -*- coding: utf-8 -*-
from plone import api

import logging
import sys
import transaction


logger = logging.getLogger("Install plugin")
logger.setLevel(logging.INFO)
ch = logging.StreamHandler(sys.stdout)
ch.setLevel(logging.INFO)
formatter = logging.Formatter(
    "%(asctime)s %(levelname)s %(name)s %(message)s", "%Y-%m-%d %H:%M:%S"
)
ch.setFormatter(formatter)
logger.addHandler(ch)


if __name__ == "__main__":
    plugin_profile = "profile-pas.plugins.imio:default"
    portal_setup = api.portal.get_tool("portal_setup")
    portal_setup.runAllImportStepsFromProfile(plugin_profile)
    transaction.commit()
    logger.info("{0} installed".format(plugin_profile))
