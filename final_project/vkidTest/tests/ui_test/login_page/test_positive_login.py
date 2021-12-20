import allure

from tests.ui_test.base_ui import BaseCase


class TestPositive(BaseCase):

    @allure.epic('Awesome test application')
    @allure.feature('UI tests')
    @allure.story('Login Page')
    def test_login_button_on_page(self):
        login_button = self.login_page.locators.LOGIN_BUTTON
        self.main_page.find(login_button)

    @allure.epic('Awesome test application')
    @allure.feature('UI tests')
    @allure.story('Login Page')
    def test_click_create_account(self):
        with allure.step("Click on link Create an account"):
            self.login_page.click(self.login_page.locators.CREATE_LINK)
        assert self.base_url + self.registration_page.route == self.driver.current_url
