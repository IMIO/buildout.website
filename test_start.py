# -*- coding: utf-8 -*-
from compose.cli.main import project_from_options
from compose.cli.main import TopLevelCommand

import docker
import os.path
import pytest
import time

options = {
    '--detach': True,
    '--no-deps': False,
    '--abort-on-container-exit': False,
    'SERVICE': '',
    '--remove-orphans': False,
    '--no-recreate': True,
    '--force-recreate': False,
    '--build': False,
    '--no-build': False,
    '--no-color': False,
    '--rmi': 'none',
    '--volumes': '',
    '--follow': False,
    '--timestamps': False,
    '--tail': 'all',
    '--always-recreate-deps': False,
    '--scale': ['instance=1', 'zeo=1'],
}


@pytest.fixture(scope='session')
def docker_compose(request):
    """
    :type request: _pytest.python.FixtureRequest
    """
    project = project_from_options(os.path.dirname(__file__), options)
    cmd = TopLevelCommand(project)
    cmd.up(options)

    def finalize():
        cmd.down(options)

    request.addfinalizer(finalize)


def test_start_instance(docker_compose):
    project = project_from_options(os.path.dirname(__file__), options)
    cmd = TopLevelCommand(project)
    instance = [
        serv for serv in cmd.project.services if serv.name == 'instance'][0]
    container_name = f'{instance.project}_{instance.name}_1'
    client = docker.from_env()
    container = client.containers.get(container_name)
    is_zope_ready = False
    timeout = time.time() + 60
    while not is_zope_ready:
        time.sleep(1)
        if container not in client.containers.list():
            print('Instance container is down, it must restart')
            break
        bytes_logs = container.logs()
        logs = bytes_logs.decode(encoding='utf-8', errors='strict')
        if 'Zope Ready to handle requests' in logs:
            is_zope_ready = True
            print('Zope Ready to handle requests !')
            continue
        if time.time() > timeout:
            print('Timeout')
            break
    assert is_zope_ready
