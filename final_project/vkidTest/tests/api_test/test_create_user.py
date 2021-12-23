import allure

from src.utils.user_builder import username, password, email
from tests.api_test.base_api import ApiBase


class TestApiCreate(ApiBase):

    @allure.epic('Awesome test application')
    @allure.feature('API tests')
    @allure.story('Create user')
    def test_success_create(self):
        res = self.api_client.create_user(username, password, email)
        assert res.status_code == 201, f"Expected status code: 201, but actual {res.status_code}. " \
                                       f"\n Response:\n\t Status:{res.status_code} \n\t Text: {res.text}"

    @allure.epic('Awesome test application')
    @allure.feature('API tests')
    @allure.story('Create user')
    def test_user_exist(self, get_random_user):
        user = get_random_user
        res = self.api_client.create_user(user["username"], user["password"], user["email"])
        assert res.status_code == 304, f"Expected status code: 304, but actual {res.status_code}. " \
                                       f"\n Response:\n\t Status:{res.status_code} \n\t Text: {res.text}"

    @allure.epic('Awesome test application')
    @allure.feature('API tests')
    @allure.story('Create user')
    def test_email_without_dog(self):
        res = self.api_client.create_user(username, password, email.replace("@", ""))
        assert res.status_code == 400, f"Expected status code: 400, but actual {res.status_code}. " \
                                       f"\n Response:\n\t Status:{res.status_code} \n\t Text: {res.text}"
