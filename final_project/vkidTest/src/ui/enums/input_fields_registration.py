from enum import Enum

from src.ui.locators.registration_locators import RegistrationLocators


class InputFields(Enum):
    username = RegistrationLocators.USERNAME_LOCATOR
    email = RegistrationLocators.EMAIL_LOCATOR
    password = RegistrationLocators.PASSWORD_LOCATOR
    repeat_password = RegistrationLocators.REPEAT_PASSWORD_LOCATOR
