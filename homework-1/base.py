import pytest
from selenium.webdriver.support.wait import WebDriverWait
import credentials
from ui.locators import basic_locators
from selenium.webdriver.support import expected_conditions as EC


class BaseCase:
    driver = None
    USER_MAIL = credentials.USER_MAIL
    USER_PASSWORD = credentials.USER_PASSWORD

    @pytest.fixture(scope='function', autouse=True)
    def setup(self, driver):
        self.driver = driver
        self.driver.implicitly_wait(10)

    def find(self, locator):
        return self.driver.find_element(*locator)

    def locator_with_href(self, text_href, locator: basic_locators):
        return locator[0], locator[1].replace('same_href', text_href)

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

    def is_button_active(self, locator, target_attribute_name="class",
                         target_attribute_value="center-module-activeButton"):
        WebDriverWait(self.driver, 10).until(EC.visibility_of_element_located(locator))
        return target_attribute_value in self.find(locator).get_attribute(target_attribute_name)

    @pytest.fixture()
    def login(self):
        if self.find(basic_locators.LOGIN_LOCATORS).is_displayed():
            self.click(basic_locators.LOGIN_LOCATORS)
            self.input(basic_locators.NAME, self.USER_MAIL)
            self.input(basic_locators.PASSWORD, self.USER_PASSWORD)
            self.click(basic_locators.AUTH_FORM_LOCATORS)
