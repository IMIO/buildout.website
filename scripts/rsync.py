#!/usr/bin/env python
# -*- coding: utf-8 -*-
import argparse
import json
import os
import signal
import subprocess
import sys
import urllib


def sigint_handler(signum, frame):
    print 'Stop pressing the CTRL+C!'
    sys.exit(0)


signal.signal(signal.SIGINT, sigint_handler)


def get_bool(prompt, default='y'):
    other = 'n' if default == 'y' else 'y'
    prompt = prompt+' ({0}/{1}) '.format(default.upper(), other)
    while True:
        value = raw_input(prompt).lower() or default
        if value in ['y', 'yes', 'oui']:
            return True
        elif value in ['n', 'no', 'non']:
            return False
        else:
            print 'Invalid input please enter y or n !'


def manage_args():
    parser = argparse.ArgumentParser()
    parser.add_argument('-i', '--municipality-id', dest='municipality_id',
                        type=str,
                        help='Id of municipailit (liege, namur, ..)')

    parse_args = parser.parse_args()
    # TODO getting from .env
    municipality_id = parse_args.municipality_id
    if not municipality_id:
        municipality_id = os.path.basename(os.getcwd())
        resp = get_bool(
            'Is "{0}" municipality you working on ?'.format(
                municipality_id))
        if not resp:
            municipality_id = raw_input(
                'What is municipality id you are going to work: ')
            municipality_id = municipality_id.replace(' ', '')
    return municipality_id


def get_rsync_server_path(municipality_id):
    url = 'http://infra-api.imio.be/application/{0}/website/production'.format(
        municipality_id
    )
    result = json.load(urllib.urlopen(url))
    if len(result) < 0:
        print 'Error in {0}'.format(url)
        return 0
    server = result[0].get('host')
    if 'lan' not in server:
        server = server.replace('imio.be', 'lan.imio.be')
    return server


def rsync(rsync_server, municipality_id):
    # test ssh access :
    test_cmd = [
        'ssh',
        '-oBatchMode=yes',
        'imio@{0}'.format(rsync_server), 'ls -l'
    ]
    try:
        subprocess.check_output(test_cmd)
    except subprocess.CalledProcessError:
        print 'You have no right to rsync on {0}, copy this line and give it to an admin:'.format(rsync_server)  # noqa
        id_rsa_pub_cmd = [
            'cat',
            '{0}/.ssh/id_rsa.pub'.format(os.environ.get('HOME'))
        ]
        id_rsa = subprocess.check_output(id_rsa_pub_cmd)
        print 'echo "{1}" | ssh imio@{0} "cat >> .ssh/authorized_keys"'.format(
           rsync_server,
           id_rsa.rstrip('\r\n')
        )
        return 0
    rsync_server_path = 'imio@{0}:/srv/instances/{1}'.format(
        rsync_server,
        municipality_id
    )
    os.system(
        'rsync -avP {0}/filestorage/Data.fs var/filestorage/Data.fs'.format(
            rsync_server_path))
    os.system(
        'rsync -r --info=progress2 {0}/blobstorage/ var/blobstorage/'.format(
            rsync_server_path))


if __name__ == '__main__':
    if get_bool('Do you want to get data ?', 'n'):
        municipality_id = manage_args()
        server = get_rsync_server_path(municipality_id)
        if server:
            rsync(server, municipality_id)
