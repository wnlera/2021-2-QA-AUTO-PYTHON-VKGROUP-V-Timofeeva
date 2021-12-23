import logging

import allure
import pytest
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from webdriver_manager.chrome import ChromeDriverManager
from webdriver_manager.firefox import GeckoDriverManager

from src.ui.pages.login_page import LoginPage
from src.ui.pages.main_page import MainPage
from src.ui.pages.registration_page import RegistrationPage


@pytest.fixture
def login_page(driver):
    return LoginPage(driver=driver)


@pytest.fixture
def main_page(driver):
    return MainPage(driver=driver)


@pytest.fixture
def registration_page(driver):
    return RegistrationPage(driver=driver)


def get_driver(config, download_dir=None):
    browser_name = config['browser']
    selenoid = config['selenoid']
    vnc = config['vnc']

    if browser_name == 'chrome':
        options = Options()
        if download_dir is not None:
            options.add_experimental_option("prefs", {"download.default_directory": download_dir,
                                                      "download.prompt_for_download": False,
                                                      "download.directory_upgrade": True,
                                                      "safebrowsing.enabled": True})
        if selenoid:
            options.add_experimental_option("prefs", {"download.default_directory": 'D:\\selenium\\Downloads'})
            capabilities = {
                'browserName': 'chrome',
                'version': '96.0' + '_VNC' if vnc else '',
                'selenoid:options':
                    {
                        'enableVNC': vnc,
                        'enableVideo': False
                    }
            }
            browser = webdriver.Remote(selenoid, desired_capabilities=capabilities)
        else:
            manager = ChromeDriverManager(version='latest', log_level=logging.CRITICAL)
            browser = webdriver.Chrome(executable_path=manager.install(), options=options)

    elif browser_name == 'firefox':
        manager = GeckoDriverManager(version='latest')
        browser = webdriver.Firefox(executable_path=manager.install())
    else:
        raise RuntimeError(f'Unsupported browser: {browser_name}')

    browser.maximize_window()
    return browser


@pytest.fixture(scope='function')
def driver(config, temp_dir, base_url):
    url = base_url
    with allure.step('Init browser'):
        browser = get_driver(config, download_dir=temp_dir)
        browser.get(url)

    yield browser
    browser.quit()
