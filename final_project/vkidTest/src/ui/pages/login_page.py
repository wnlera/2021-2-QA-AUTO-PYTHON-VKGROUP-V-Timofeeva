import allure

from src.ui.locators.login_locators import LoginLocators
from src.ui.pages.base_page import BasePage
from src.ui.enums.input_fields_login import InputFields


class LoginPage(BasePage):
    route = "/login"
    locators = LoginLocators()
    
    @allure.step('Write the value {input_value} in the field {field}')
    def input_field(self, field: InputFields, input_value):
        self.input(field, input_value)

    @allure.step('Get value {input_value} from the field {field}')
    def get_value_from_field(self, field: InputFields):
        input_field = self.find(field)
        return input_field.text()

    @allure.step('Click on login button')
    def click_login(self, username, password):
        self.input_field(self.locators.USERNAME_LOCATOR, username)
        self.input_field(self.locators.PASSWORD_LOCATOR, password)
        self.click(self.locators.LOGIN_BUTTON)
