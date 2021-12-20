import time

import allure

from src.ui.locators.registration_locators import RegistrationLocators
from src.ui.pages.base_page import BasePage
from src.ui.enums.input_fields_registration import InputFields


class RegistrationPage(BasePage):
    route = "/reg"
    locators = RegistrationLocators()

    @allure.step('Write the value {input_value} in the field {field}')
    def input_field(self, field: InputFields, input_value):
        self.input(field.value, input_value)

    @allure.step('Get value {input_value} from the field {field}')
    def get_value_from_field(self, field: InputFields):
        input_field = self.find(field)
        return input_field.text()

    @allure.step('Get default accept checkbox state')
    def get_checkbox_state(self):
        accept = self.find(self.locators.ACCEPT_LOCATOR)
        return self.checkbox_is_selected(accept)

    @allure.step('Try registred:'
                 'usernsme: {username_value},'
                 'email: {email_value},'
                 'password: {password_value}'
                 'repeat password: {repeat_value}')
    def register(self, username_value, email_value, password_value, repeat_value, accept_agreement=True):
        register_button = self.find(self.locators.REGISTER_BUTTON)
        self.input_field(InputFields.username, username_value)
        self.input_field(InputFields.email, email_value)
        self.input_field(InputFields.password, password_value)
        self.input_field(InputFields.repeat_password, repeat_value)
        if accept_agreement:
            self.click(self.locators.ACCEPT_LOCATOR)
        self.click(register_button)
