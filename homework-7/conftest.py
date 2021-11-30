import os
import signal
import subprocess
import sys
import time
from copy import copy
import pytest

import requests
from requests.exceptions import ConnectionError

import settings
from client.mock_client import ApiClient

repo_root = os.path.abspath(os.path.join(__file__, os.pardir))


def wait_ready(host, port):
    started = False
    st = time.time()
    while time.time() - st <= 5:
        try:
            requests.get(f'http://{host}:{port}')
            started = True
            break
        except ConnectionError:
            pass

    if not started:
        raise RuntimeError(f'{host}:{port} did not started in 5s!')


def pytest_configure(config):
    if not hasattr(config, 'workerinput'):
        app_path = os.path.join(repo_root, 'application', 'app.py')

        env = copy(os.environ)
        env.update({
            'APP_HOST': settings.APP_HOST,
            'APP_PORT': settings.APP_PORT,
            'NUMBER_HOST': settings.MOCK_HOST,
            'NUMBER_PORT': settings.MOCK_PORT
        })
        try:
            app_stderr = open('homework-7/tmp/app_stderr', 'w')
            app_stdout = open('homework-7/tmp/app_stdout', 'w')
        except FileNotFoundError:
            app_stderr = open('../tmp/app_stderr', 'w')
            app_stdout = open('../tmp/app_stdout', 'w')

        app_proc = subprocess.Popen([sys.executable, app_path],
                                    stderr=app_stderr, stdout=app_stdout,
                                    env=env, shell=False)
        wait_ready(settings.APP_HOST, settings.APP_PORT)

        config.app_proc = app_proc
        config.app_stderr = app_stderr
        config.app_stdout = app_stdout

        from mock import flask_mock
        flask_mock.run_mock()

        wait_ready(settings.MOCK_HOST, settings.MOCK_PORT)


def pytest_unconfigure(config):
    requests.get(f'http://{settings.APP_HOST}:{settings.APP_PORT}/shutdown')
    config.app_stderr.close()
    config.app_stdout.close()

    requests.get(f'http://{settings.MOCK_HOST}:{settings.MOCK_PORT}/shutdown')


@pytest.fixture(scope='session')
def api_client():
    return ApiClient()
