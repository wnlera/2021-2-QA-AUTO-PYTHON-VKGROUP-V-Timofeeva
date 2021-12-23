import random
from faker import Faker
import pytest


class ApiBase:
    @pytest.fixture(scope='function', autouse=True)
    def setup(self, api_client):
        self.api_client = api_client

    @pytest.fixture(scope='function')
    def get_random_user(self):
        faker = Faker()
        users = []
        for x in range(10):
            username = faker.profile()["username"]
            email = faker.profile()["mail"]
            password = faker.password()
            res = self.api_client.create_user(username, password, email)
            users.append({'username': username,
                          'password': password,
                          'email': email})
        return users[random.randint(0, len(users)-1)]
