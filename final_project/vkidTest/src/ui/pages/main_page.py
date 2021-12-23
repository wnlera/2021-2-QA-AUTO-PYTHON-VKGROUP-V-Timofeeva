import allure

from src.ui.locators.main_page_locators import MainPageLocators
from src.ui.pages.base_page import BasePage


class MainPage(BasePage):
    route = "/welcome/"
    locators = MainPageLocators()

    @allure.step('Going to {event}')
    def do_logout(self):
        logout_button = self.find(self.locators.LOGOUT_BUTTON)
        self.click(logout_button)