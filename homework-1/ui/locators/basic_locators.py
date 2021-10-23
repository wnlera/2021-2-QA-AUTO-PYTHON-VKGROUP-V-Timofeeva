from selenium.webdriver.common.by import By


LOGIN_LOCATORS = (By.XPATH, "//div[starts-with(@class, 'responseHead-module-button')]")
NAME = (By.NAME, "email")
PASSWORD = (By.NAME, "password")
AUTH_FORM_LOCATORS = (By.XPATH, "//div[starts-with(@class, 'authForm-module-button')]")
USER_RIGHT_BUTTON = (By.XPATH, "//div[starts-with(@class, 'right-module-rightButton')]")
LOGOUT_BUTTON = (By.XPATH, "//a[@href = '/logout']")
PROFILE = (By.XPATH, "//a[@href = '/profile']")
CONTACT_INFO = (By.XPATH, "//a[@href = '/profile/contacts']")
USER_NAME = (By.CSS_SELECTOR, "div[data-name = 'username']")
FIO = (By.CSS_SELECTOR, "div[data-name = 'fio'] input")
SAVE_CONTACT = (By.CSS_SELECTOR, "button[data-class-name = 'Submit']")
HOME_BUTTON = (By.XPATH, "//a[@href = '//target.my.com']")
MENU_BUTTON = (By.XPATH, "//a[text()='same_text']")

