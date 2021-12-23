import allure

from tests.ui_test.base_ui import BaseCase
from src.utils.user_builder import username, password


class TestNegative(BaseCase):

    @allure.epic('Awesome test application')
    @allure.feature('UI tests')
    @allure.story('Login Page')
    @allure.tag('Negative tests')
    def test_click_login_user_not_registered(self):
        with allure.step("Input username, password and click on Create Login"):
            self.login_page.click_login(username + "t", password)
        assert self.login_page.get_text(self.login_page.locators.ERROR_FLASH) == "Invalid username or password"
