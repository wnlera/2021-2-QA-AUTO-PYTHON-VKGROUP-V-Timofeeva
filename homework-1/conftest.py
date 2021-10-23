import pytest
from selenium import webdriver
from selenium.webdriver.chrome.service import Service


def pytest_addoption(parser):
    parser.addoption('--browser', default='chrome')
    parser.addoption('--url', default='https://target.my.com/')


@pytest.fixture()
def config(request):
    browser = request.config.getoption('--browser')
    url = request.config.getoption('--url')

    return {'browser': browser, 'url': url}


@pytest.fixture(scope='function')
def driver(config):

    browser = config['browser']
    url = config['url']

    service = Service(r"D:\ProgrammingProjects\PythonProj\drivers\chromedriver_win32\chromedriver.exe")
    service.start()
    browser = webdriver.Remote(service.service_url)
    browser.maximize_window()
    browser.get(url)

    yield browser
    browser.close()
