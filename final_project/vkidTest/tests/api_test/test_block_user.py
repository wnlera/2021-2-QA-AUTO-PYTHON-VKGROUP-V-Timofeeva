import pytest
import allure

from tests.api_test.base_api import ApiBase


class TestApiBlock(ApiBase):

    @allure.epic('Awesome test application')
    @allure.feature('API tests')
    @allure.story('Block user')
    def test_success_block(self, get_random_user):
        name = get_random_user["username"]
        res = self.api_client.block_user(name)
        assert res.status_code == 200, f"Expected status code: 200, but actual {res.status_code}. " \
                                       f"\n Responce:\n\t Status:{res.status_code} \n\t Text: {res.text}"

    @allure.epic('Awesome test application')
    @allure.feature('API tests')
    @allure.story('Block user')
    def test_try_block_after_block(self, get_random_user):
        name = get_random_user["username"]
        self.api_client.block_user(name)
        res = self.api_client.block_user(name)
        assert res.status_code == 304, f"Expected status code: 304, but actual {res.status_code}. " \
                                       f"\n Responce:\n\t Status:{res.status_code} \n\t Text: {res.text}"

    @allure.epic('Awesome test application')
    @allure.feature('API tests')
    @allure.story('Block user')
    def test_delete_not_exist_user(self, get_random_user):
        name = get_random_user["username"]
        res = self.api_client.delete_user(name + "1")
        assert res.status_code == 404, f"Expected status code: 404, but actual {res.status_code}. " \
                                       f"\n Responce:\n\t Status:{res.status_code} \n\t Text: {res.text}"