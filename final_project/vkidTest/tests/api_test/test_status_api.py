import pytest
import allure

from tests.api_test.base_api import ApiBase


class TestApiStatus(ApiBase):
    @allure.epic('Awesome test application')
    @allure.feature('API tests')
    @allure.story('Status api')
    def test_success_status(self):
        res = self.api_client.get_status()
        assert res.status_code == 200, f"Expected status code: 200, but actual {res.status_code}."
