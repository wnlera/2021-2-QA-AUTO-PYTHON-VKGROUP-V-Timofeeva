import logging

import allure
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.wait import WebDriverWait

CLICK_RETRY = 3
BASE_TIMEOUT = 10


class PageNotLoadedException(Exception):
    pass


class BasePage(object):

    def __init__(self, driver):
        self.driver = driver
        self.logger = logging.getLogger('test')
        self.driver.implicitly_wait(10)

    def find(self, locator):
        return self.driver.find_element(*locator)

    def input(self, locator, input_str):
        field = self.find(locator)
        field.send_keys(input_str)

    def checkbox_is_selected(self, locator):
        checkbox = self.find(locator)
        return checkbox.is_selected()

    def get_text(self, locator):
        WebDriverWait(self.driver, 3).until(EC.visibility_of_element_located(locator))
        return self.find(locator).text

    @allure.step('Clicking on {locator}')
    def click(self, locator, attempts=8):
        self.logger.info(f'Clicking on {locator}')
        for x in range(attempts+1):
            try:
                WebDriverWait(self.driver, 10).until(EC.element_to_be_clickable(locator)).click()
            except:
                if x > attempts:
                    raise
            else:
                break