import time

import pytest
from selenium.webdriver.support.wait import WebDriverWait

from ui.locators import basic_locators
from selenium.webdriver.support import expected_conditions as EC


class BaseCase:
    driver = None
    USER_MAIL = "testiruyushchiy@inbox.ru"
    USER_PASSWORD = "bH+fUYviRZ8rbuH"

    @pytest.fixture(scope='function', autouse=True)
    def setup(self, driver):
        self.driver = driver
        self.driver.implicitly_wait(10)

    def find(self, locator):
        return self.driver.find_element(*locator)

    def locator_with_text(self, text, locator: basic_locators):
        return locator[0], locator[1].replace('same_text', text)

    def input(self, locator, input_str):
        search = self.find(locator)
        search.send_keys(input_str)

    def click(self, locator, attempts=8):
        for x in range(attempts+1):
            try:
                WebDriverWait(self.driver, 10).until(EC.element_to_be_clickable(locator)).click()
            except:
                if x > attempts:
                    raise
            else:
                break

    def is_button_active(self, locator):
        WebDriverWait(self.driver, 10).until(EC.visibility_of_element_located(locator))
        if "center-module-activeButton" in self.find(locator).get_attribute("class"):
            return True
        else:
            return False

    @pytest.fixture()
    def login(self):
        if self.find(basic_locators.LOGIN_LOCATORS).is_displayed():
            self.click(basic_locators.LOGIN_LOCATORS)
            self.input(basic_locators.NAME, self.USER_MAIL)
            self.input(basic_locators.PASSWORD, self.USER_PASSWORD)
            self.click(basic_locators.AUTH_FORM_LOCATORS)
