from base import BaseCase
from ui.locators import basic_locators
from ui import page_routes
import pytest


class TestUI(BaseCase):

    @pytest.mark.ui
    def test_login(self):
        user_mail: str = "testiruyushchiy@inbox.ru"
        self.click(basic_locators.LOGIN_LOCATORS)
        self.input(basic_locators.NAME, user_mail)
        self.input(basic_locators.PASSWORD, "bH+fUYviRZ8rbuH")
        self.click(basic_locators.AUTH_FORM_LOCATORS)
        self.click(basic_locators.PROFILE)
        self.click(basic_locators.CONTACT_INFO)
        assert self.find(basic_locators.USER_NAME).text == user_mail

    @pytest.mark.ui
    def test_logout(self, login):
        self.click(basic_locators.USER_RIGHT_BUTTON)
        self.click(basic_locators.LOGOUT_BUTTON)
        self.find(basic_locators.LOGIN_LOCATORS).is_displayed()

    @pytest.mark.ui
    def test_contact_info(self, login):
        user_fio: str = "Тест Тестирующий"
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
        'page',
        [
            pytest.param(
                'Баланс'
            ),
            pytest.param(
                'Инструменты'
            )
        ]
    )
    @pytest.mark.ui
    def test_pages(self, page, login):
        self.click(self.locator_with_text(page, basic_locators.MENU_BUTTON))
        current_url = self.driver.current_url
        assert page_routes.PAGE[page] in current_url
        #так можно проверить изменившийся UI, выбранная вкладка становится серой
        # assert "center-module-activeButton" in self.find_by_text(page.NAME, basic_locators.MENU_BUTTON).get_attribute("class")







