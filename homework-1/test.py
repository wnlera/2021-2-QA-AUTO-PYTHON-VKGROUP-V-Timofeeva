from base import BaseCase
from ui.locators import basic_locators
import pytest
from rand_string import get_random_string


class TestUI(BaseCase):
    @pytest.mark.UI
    def test_login(self):
        user_mail: str = BaseCase.USER_MAIL
        self.click(basic_locators.LOGIN_LOCATORS)
        self.input(basic_locators.NAME, user_mail)
        self.input(basic_locators.PASSWORD, BaseCase.USER_PASSWORD)
        self.click(basic_locators.AUTH_FORM_LOCATORS)
        self.click(basic_locators.PROFILE)
        self.click(basic_locators.CONTACT_INFO)
        assert self.find(basic_locators.USER_NAME).text == user_mail

    @pytest.mark.UI
    def test_logout(self, login):
        self.click(basic_locators.USER_RIGHT_BUTTON)
        self.click(basic_locators.LOGOUT_BUTTON)
        self.find(basic_locators.LOGIN_LOCATORS).is_displayed()

    @pytest.mark.UI
    def test_contact_info(self, login):
        user_fio = f"{get_random_string(3, 10, True)} {get_random_string(3, 10, True)}"
        self.click(basic_locators.PROFILE)
        self.click(basic_locators.CONTACT_INFO)
        self.find(basic_locators.FIO).clear()
        self.find(basic_locators.FIO).send_keys(user_fio)
        self.click(basic_locators.SAVE_CONTACT)
        self.click(basic_locators.HOME_BUTTON)
        self.click(basic_locators.PROFILE)
        self.click(basic_locators.CONTACT_INFO)
        assert self.find(basic_locators.FIO).get_attribute("value") == user_fio

    @pytest.mark.parametrize(
        'page_href',
        [
            pytest.param(
                '/billing'
            ),
            pytest.param(
                '/tools'
            )
        ]
    )
    @pytest.mark.UI
    def test_pages(self, page_href, login):
        menu_button = self.locator_with_href(page_href, basic_locators.MENU_BUTTON)
        self.click(menu_button)
        current_url = self.driver.current_url
        assert page_href in current_url
        #так можно проверить изменившийся UI, выбранная вкладка становится серой
        assert self.is_button_active(menu_button)
