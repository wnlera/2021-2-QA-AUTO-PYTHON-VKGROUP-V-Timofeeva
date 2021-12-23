import time

import allure
from src.utils.user_builder import username, password, email
from tests.ui_test.base_ui import BaseCase


class TestUserInfo(BaseCase):
    @allure.epic('Awesome test application')
    @allure.feature('UI tests')
    @allure.story('Main Page')
    @allure.tag('Positive test')
    def test_login_info_on_page(self):
        with allure.step("Go to registration page"):
            self.login_page.click(self.login_page.locators.CREATE_LINK)
        with allure.step("Registration user"):
            self.registration_page.register(username, email, password, password)
        user = self.main_page.locators.LOGINNAME_LOCATOR
        assert self.main_page.get_text(user) == f"Logged as {username}"

    @allure.epic('Awesome test application')
    @allure.feature('UI tests')
    @allure.story('Main Page')
    @allure.tag('Positive test')
    def test_vk_id_on_page(self):
        new_user = username + "a"
        with allure.step("Create VK ID"):
            self.create_vk_id(new_user)
        with allure.step("Go to registration page"):
            self.login_page.click(self.login_page.locators.CREATE_LINK)
        with allure.step("Registration user"):
            self.registration_page.register(new_user, email + "a", password, password)
        user = self.main_page.locators.LOGINNAME_LOCATOR_LI
        vk_id = self.main_page.locators.VKID_LOCATOR_LI
        assert self.main_page.get_text(user) == f"Logged as {new_user}"
        assert self.main_page.get_text(vk_id) == f"VK ID: {self.get_vk_id(new_user)}"
