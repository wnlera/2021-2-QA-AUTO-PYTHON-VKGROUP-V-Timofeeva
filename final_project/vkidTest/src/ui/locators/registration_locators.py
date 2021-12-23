from selenium.webdriver.common.by import By


class RegistrationLocators:
    USERNAME_LOCATOR = (By.ID, "username")
    EMAIL_LOCATOR = (By.ID, "email")
    PASSWORD_LOCATOR = (By.ID, "password")
    REPEAT_PASSWORD_LOCATOR = (By.ID, "confirm")
    ACCEPT_LOCATOR = (By.XPATH, "//input[@id = 'term']")
    REGISTER_BUTTON = (By.ID, "submit")
    LOGIN_LINK = (By.XPATH, "//a[@href = '/login']")
    ERROR_FLASH = (By.XPATH, "//div[contains(@class, 'uk-alert')]")
