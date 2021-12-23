from selenium.webdriver.common.by import By


class MainPageLocators:

    LOGOUT_BUTTON = (By.XPATH, "//a[@href = '/logout']")
    LOGINNAME_LOCATOR = (By.ID, "login-name")

    LOGINNAME_LOCATOR_LI = (By.XPATH, "//div[@id ='login-name']//li[1]")
    VKID_LOCATOR_LI = (By.XPATH, "//div[@id ='login-name']//li[2]")
    NAVBAR_ROOT = (By.XPATH, "//a[contains(@class, 'uk-navbar-brand uk-hidden-small')]")
    NAVBAR_HOME = (By.XPATH, "//a[. = 'HOME']")
    NAVBAR_PYTHON = (By.XPATH, "//a[. = 'Python']")
    NAVBAR_LINUX = (By.XPATH, "//a[. = 'Linux']")
    NAVBAR_NETWORK = (By.XPATH, "//a[. = 'Network']")

    API_HEADER = (By.XPATH, "//div[. = 'What is an API?']")
    API_LINK = (By.XPATH, "//a[. = 'https://en.wikipedia.org/wiki/Application_programming_interface']")
    API_IMG = (By.XPATH, "//img[contains(@src, 'laptop')]")

    FEATURE_HEADER = (By.XPATH, "//div[. = 'Future of internet']")
    FEATURE_LINK = (By.XPATH, "//a[contains(@href,'https://www.popularmechanics.com/technology/')]")
    FEATURE_IMG = (By.XPATH, "//img[contains(@src, 'loupe')]")

    SMTP_HEADER = (By.XPATH, "//div[. = 'Lets talk about SMTP?']")
    SMTP_LINK = (By.XPATH, "//a[. = 'https://ru.wikipedia.org/wiki/SMTP']")
    SMTP_IMG = (By.XPATH, "//img[contains(@src, 'analytics')]")
