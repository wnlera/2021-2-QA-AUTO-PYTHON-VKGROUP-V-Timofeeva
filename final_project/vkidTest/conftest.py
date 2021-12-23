import os
import shutil
import sys
import subprocess
import time

import requests

from src.api.client import ApiClient
from src.api.mock_client import ApiMockClient
from src.db.client import MysqlORMClient
from src.ui.fixtures import *
from src.credentials.credentials_db import USER, PASSWORD

MOCK_URL = 'http://localhost:5001'
BASE_URL_SELENOID = 'http://vk_app:5002'
BASE_URL = 'http://localhost:5002'


def pytest_addoption(parser):
    parser.addoption('--browser', default='chrome')
    parser.addoption('--url', default=BASE_URL)
    parser.addoption('--selenoid', action='store_true')
    parser.addoption('--vnc', action='store_true')
    parser.addoption('--debug_log', action='store_true')


@pytest.fixture(scope='session')
def config(request):
    browser = request.config.getoption('--browser')
    url = request.config.getoption('--url')
    debug_log = request.config.getoption('--debug_log')
    if request.config.getoption('--selenoid'):
        selenoid = 'http://localhost:4444/wd/hub'
        if request.config.getoption('--vnc'):
            vnc = True
        else:
            vnc = False
    else:
        selenoid = None
        vnc = False

    return {'browser': browser, 'url': url,
            'debug_log': debug_log, 'selenoid': selenoid, 'vnc': vnc}


@pytest.fixture(scope='function')
def logger(temp_dir, config):
    log_formatter = logging.Formatter('%(asctime)s - %(filename)s - %(levelname)s - %(message)s')
    log_file = os.path.join(temp_dir, 'test.log')
    log_level = logging.DEBUG if config['debug_log'] else logging.INFO

    file_handler = logging.FileHandler(log_file, 'w')
    file_handler.setFormatter(log_formatter)
    file_handler.setLevel(log_level)

    log = logging.getLogger('test')
    log.propagate = False
    log.setLevel(log_level)
    log.handlers.clear()
    log.addHandler(file_handler)

    yield log

    for handler in log.handlers:
        handler.close()

    with open(log_file, 'r') as f:
        allure.attach(f.read(), 'test.log', attachment_type=allure.attachment_type.TEXT)


def pytest_configure(config):
    if sys.platform.startswith('win'):
        base_dir = 'D:\\tests'
    else:
        base_dir = '/tmp/tests'

    if not hasattr(config, 'workerinput'):  # in master only
        if os.path.exists(base_dir):
            shutil.rmtree(base_dir)

        os.makedirs(base_dir)

    config.base_temp_dir = base_dir
    try:
        app_stderr = open('tmp/up_stderr', 'w')
        app_stdout = open('tmp/up_stdout', 'w')
    except FileNotFoundError:
        app_stderr = open('../../../tmp/up_stderr', 'w')
        app_stdout = open('../../../tmp/up_stdout', 'w')
    up = subprocess.Popen("docker compose -f ../docker-compose.yml up -d", stderr=app_stderr, stdout=app_stdout)
    print("Wait for containers...")
    exit_code = up.wait(260)
    if exit_code == 0:
        print("Containers are ready")
    else:
        raise Exception("Unable to create containers")
    time.sleep(10)  # wait for db container
    if not wait_for_app(config):
        raise Exception("App not started")
    config.up = up
    config.app_stderr = app_stderr
    config.app_stdout = app_stdout
    mysql_orm_client = MysqlORMClient(user=USER, password=PASSWORD, db_name="TEST_DB")
    config.mysql_orm_client = mysql_orm_client
    config.mysql_orm_client.connect()


def wait_for_app(config, retry=30, delay_sec=2):
    success_needed = 3
    success = 0
    # url = f"{config['url']}/api/status"
    url = f"http://localhost:5002/status"
    print(url)
    for i in range(retry):
        print(f"wait for app {i}")
        check = None
        try:
            check = requests.get(url)
        except Exception as e:
            print(e)
            pass

        if check: #and check.status_code == 200:
            return True
        time.sleep(delay_sec)
    return False



@pytest.fixture(scope='session')
def mysql_orm_client(request) -> MysqlORMClient:
    client = request.config.mysql_orm_client
    yield client
    client.connection.close()


@pytest.fixture(scope='function')
def temp_dir(request):
    test_dir = os.path.join(request.config.base_temp_dir,
                            request._pyfuncitem.nodeid.replace('/', '_').replace(':', '_'))
    os.makedirs(test_dir)
    return test_dir


@pytest.fixture(scope='session')
def repo_root():
    return os.path.abspath(os.path.join(__file__, os.path.pardir))


@pytest.fixture(scope='session')
def api_client(config):
    return ApiClient(config['url'])


@pytest.fixture(scope='session')
def api_mock_client(config):
    return ApiMockClient(MOCK_URL)

@pytest.fixture(scope='function')
def base_url(config):
    if config["selenoid"] is None:
        return BASE_URL
    else:
        return BASE_URL_SELENOID


def pytest_unconfigure(config):
    return
    try:
        down_stderr = open('tmp/down_stderr', 'w')
        down_stdout = open('tmp/down_stdout', 'w')
    except FileNotFoundError:
        down_stderr = open('tmp/down_stderr', 'w')
        down_stdout = open('tmp/down_stdout', 'w')
    down = subprocess.Popen("docker compose -f ../docker-compose.yml down", stderr=down_stderr, stdout=down_stdout)
    down.wait(90)
    config.app_stderr.close()
    config.app_stdout.close()
    down_stderr.close()
    down_stdout.close()
    os.system("allure serve allure_reports")
