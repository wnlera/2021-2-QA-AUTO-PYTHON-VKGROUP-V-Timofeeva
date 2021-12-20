import time

import allure

from tests.ui_test.base_ui import BaseCase
from src.utils.user_builder import username, password, email


class TestNegative(BaseCase):

    @allure.epic('Awesome test application')
    @allure.feature('UI tests')
    @allure.story('Registration page')
    @allure.tag('Positive tests')
    def test_registration_user(self):
        with allure.step("Go to registration page"):
            self.login_page.click(self.login_page.locators.CREATE_LINK)
        with allure.step("Registration user"):
            self.registration_page.register(username, email, password, password)
        time.sleep(5)
        assert self.driver.current_url == self.base_url + self.main_page.route

    @allure.epic('Awesome test application')
    @allure.feature('UI tests')
    @allure.story('Registration page')
    @allure.tag('Positive tests')
    def test_back_to_login(self):
        with allure.step("Go to registration page"):
            self.login_page.click(self.login_page.locators.CREATE_LINK)
        with allure.step("Click on Log in"):
            self.registration_page.click(self.registration_page.locators.LOGIN_LINK)
        assert self.driver.current_url == self.base_url + self.login_page.route