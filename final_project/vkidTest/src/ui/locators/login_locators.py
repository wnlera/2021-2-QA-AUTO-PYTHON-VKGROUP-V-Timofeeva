from selenium.webdriver.common.by import By


class LoginLocators:
    USERNAME_LOCATOR = (By.ID, "username")
    PASSWORD_LOCATOR = (By.ID, "password")
    LOGIN_BUTTON = (By.ID, "submit")
    CREATE_LINK = (By.XPATH, "//a[@href = '/reg']")
    ERROR_FLASH = (By.XPATH, "//div[contains(@class, 'uk-alert')]")
