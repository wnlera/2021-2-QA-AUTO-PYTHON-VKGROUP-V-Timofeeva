import random

import allure

from tests.ui_test.base_ui import BaseCase
from src.utils.user_builder import email, password, russian_name, username


class TestNegative(BaseCase):

    @allure.epic('Awesome test application')
    @allure.feature('UI tests')
    @allure.story('Registration page')
    @allure.tag("Negative tests")
    def test_cyrillic_username(self):
        with allure.step("Go to registration page"):
            self.login_page.click(self.login_page.locators.CREATE_LINK)
        with allure.step("Try create user with Cyrillic login"):
            self.registration_page.register(russian_name, email, password, password)
        assert self.login_page.get_text(self.login_page.locators.ERROR_FLASH) == "Incorrect username"

    @allure.epic('Awesome test application')
    @allure.feature('UI tests')
    @allure.story('Registration page')
    @allure.tag("Negative tests")
    def test_short_username(self):
        short_name = "abads"
        with allure.step("Go to registration page"):
            self.login_page.click(self.login_page.locators.CREATE_LINK)
        with allure.step("Try create user with short login"):
            self.registration_page.register(short_name[0: random.randint(1, 5)], email, password, password)
        assert self.login_page.get_text(self.login_page.locators.ERROR_FLASH) == "Incorrect username length"

    @allure.epic('Awesome test application')
    @allure.feature('UI tests')
    @allure.story('Registration page')
    @allure.tag("Negative tests")
    def test_short_mail(self):
        short_mail = "q@q.qq"
        name = "normuser"
        with allure.step("Go to registration page"):
            self.login_page.click(self.login_page.locators.CREATE_LINK)
        with allure.step("Try create user with short email"):
            self.registration_page.register(name, short_mail, password, password)
        assert self.login_page.get_text(self.login_page.locators.ERROR_FLASH) == "Incorrect email length"

    @allure.epic('Awesome test application')
    @allure.feature('UI tests')
    @allure.story('Registration page')
    @allure.tag("Negative tests")
    def test_short_mail_username(self):
        short_mail = "a@a.aa"
        short_name = "qqqqq"
        with allure.step("Go to registration page"):
            self.login_page.click(self.login_page.locators.CREATE_LINK)
        with allure.step("Try create user with short login and mail"):
            self.registration_page.register(short_name[0: random.randint(1, 5)], short_mail, password, password)
        assert self.login_page.get_text(
            self.login_page.locators.ERROR_FLASH) == "{'username': ['Incorrect username length'], " \
                                                     "'email': ['Incorrect email length']}"

    @allure.epic('Awesome test application')
    @allure.feature('UI tests')
    @allure.story('Registration page')
    @allure.tag("Negative tests")
    def test_password_match(self):
        with allure.step("Go to registration page"):
            self.login_page.click(self.login_page.locators.CREATE_LINK)
        with allure.step("Input different password"):
            self.registration_page.register(username, email, password, password + "a")
        assert self.login_page.get_text(self.login_page.locators.ERROR_FLASH) == "Passwords must match"

    @allure.epic('Awesome test application')
    @allure.feature('UI tests')
    @allure.story('Registration page')
    @allure.tag("Negative tests")
    def test_dont_accept(self):
        with allure.step("Go to registration page"):
            self.login_page.click(self.login_page.locators.CREATE_LINK)
        with allure.step("Do not click on checkbox"):
            self.registration_page.register(username, email, password, password, accept_agreement=False)
        assert self.driver.current_url == self.base_url + self.registration_page.route
