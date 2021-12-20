import os

import allure
import pytest
from _pytest.fixtures import FixtureRequest
from selenium.webdriver.remote.webdriver import WebDriver

from src.ui.pages.login_page import LoginPage
from src.ui.pages.main_page import MainPage
from src.ui.pages.registration_page import RegistrationPage

CLICK_RETRY = 3


class BaseCase:

    driver = None

    @pytest.fixture(scope='function', autouse=True)
    def ui_report(self, driver, request, temp_dir):
        failed_tests_count = request.session.testsfailed
        yield
        if request.session.testsfailed > failed_tests_count:
            screenshot = os.path.join(temp_dir, 'failure.png')
            driver.get_screenshot_as_file(screenshot)
            allure.attach.file(screenshot, 'failure.png', attachment_type=allure.attachment_type.PNG)

            browser_log = os.path.join(temp_dir, 'browser.log')
            with open(browser_log, 'w') as f:
                for i in driver.get_log('browser'):
                    f.write(f"{i['level']} - {i['source']}\n{i['message']}\n")

            with open(browser_log, 'r') as f:
                allure.attach(f.read(), 'browser.log', attachment_type=allure.attachment_type.TEXT)

    @pytest.fixture(scope='function', autouse=True)
    def setup(self, driver, config, logger, request: FixtureRequest, api_mock_client, base_url):
        self.driver: WebDriver = driver
        self.config = config
        self.logger = logger
        self.base_url = base_url
        self.api_mock_client = api_mock_client
        self.login_page: LoginPage = request.getfixturevalue('login_page')
        self.registration_page: RegistrationPage = request.getfixturevalue('registration_page')
        self.main_page: MainPage = request.getfixturevalue('main_page')

        self.logger.debug('Initial setup completed')

    def create_vk_id(self, username):
        res = self.api_mock_client.create_vk_id(username)
        if res.status_code == 201:
            return res.json()
        else:
            raise Exception(f"Не удалось создать VK ID для пользователя {username}. Response status: {res.status_code}")

    def get_vk_id(self, username):
        res = self.api_mock_client.get_vk_id(username)
        if res.status_code == 200:
            return res.json()["vk_id"]
        else:
            raise Exception(f"Не удалось получить VK ID для пользователя {username}. Response status: {res.status_code}")

