# -*- coding: utf-8 -*-
"""
You can start this script with a "instance run" like :
    bin/instance -O Plone run scripts/autopublish.py

"""
from plone import api

import argparse
import logging
import sys


logger = logging.getLogger('export_plone_users.py')
logger.setLevel(logging.INFO)
ch = logging.StreamHandler(sys.stdout)
ch.setLevel(logging.INFO)
formatter = logging.Formatter('%(asctime)s %(levelname)s %(name)s %(message)s',
                              '%Y-%m-%d %H:%M:%S')
ch.setFormatter(formatter)
logger.addHandler(ch)

parser = argparse.ArgumentParser(description='Run a script')
parser.add_argument('-c')  # use to bin/instance run script.py


def publish():
    portal = api.portal.get()
    result = portal.restrictedTraverse('@@tick_hourly')()
    logger.info(result)


if __name__ == '__main__':
    args = parser.parse_args()
    publish()
