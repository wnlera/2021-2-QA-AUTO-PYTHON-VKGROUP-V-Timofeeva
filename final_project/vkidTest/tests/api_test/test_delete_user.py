import pytest
import allure

from tests.api_test.base_api import ApiBase


class TestApiDelete(ApiBase):

    @allure.epic('Awesome test application')
    @allure.feature('API tests')
    @allure.story('Delete user')
    def test_success_delete(self, get_random_user):
        name = get_random_user["username"]
        res = self.api_client.delete_user(name)
        assert res.status_code == 204, f"Expected status code: 204, but actual {res.status_code}. " \
                                       f"\n Responce:\n\t Status:{res.status_code} \n\t Text: {res.text}"

    @allure.epic('Awesome test application')
    @allure.feature('API tests')
    @allure.story('Delete user')
    def test_try_delete_after_delete(self, get_random_user):
        name = get_random_user["username"]
        res = self.api_client.delete_user(name)
        res = self.api_client.delete_user(name)
        assert res.status_code == 404, f"Expected status code: 404, but actual {res.status_code}. " \
                                       f"\n Responce:\n\t Status:{res.status_code} \n\t Text: {res.text}"

    @allure.epic('Awesome test application')
    @allure.feature('API tests')
    @allure.story('Delete user')
    def test_delete_not_exist_user(self, get_random_user):
        name = get_random_user["username"]
        res = self.api_client.delete_user(name + "1")
        assert res.status_code == 404, f"Expected status code: 404, but actual {res.status_code}. " \
                                       f"\n Responce:\n\t Status:{res.status_code} \n\t Text: {res.text}"