import pytest
import allure

from tests.api_test.base_api import ApiBase


class TestApiAccept(ApiBase):

    @allure.epic('Awesome test application')
    @allure.feature('API tests')
    @allure.story('Accept user')
    def test_success_accept(self, get_random_user):
        name = get_random_user["username"]
        self.api_client.block_user(name)
        res = self.api_client.accept_user(name)
        assert res.status_code == 200, f"Expected status code: 200, but actual {res.status_code}. " \
                                       f"\n Responce:\n\t Status:{res.status_code} \n\t Text: {res.text}"

    @allure.epic('Awesome test application')
    @allure.feature('API tests')
    @allure.story('Accept user')
    def test_try_accept_after_accept(self, get_random_user):
        name = get_random_user["username"]
        self.api_client.accept_user(name)
        res = self.api_client.accept_user(name)
        assert res.status_code == 304, f"Expected status code: 304, but actual {res.status_code}. " \
                                       f"\n Responce:\n\t Status:{res.status_code} \n\t Text: {res.text}"

    @allure.epic('Awesome test application')
    @allure.feature('API tests')
    @allure.story('Accept user')
    def test_delete_not_exist_user(self, get_random_user):
        name = get_random_user["username"]
        res = self.api_client.accept_user(name + "1")
        assert res.status_code == 404, f"Expected status code: 404, but actual {res.status_code}. " \
                                       f"\n Responce:\n\t Status:{res.status_code} \n\t Text: {res.text}"