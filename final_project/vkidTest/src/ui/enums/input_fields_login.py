from enum import Enum

from src.ui.locators.login_locators import LoginLocators


class InputFields(Enum):
    username = LoginLocators.USERNAME_LOCATOR
    password = LoginLocators.PASSWORD_LOCATOR
