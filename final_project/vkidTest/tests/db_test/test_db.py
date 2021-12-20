import allure

from base_db import MysqlBase
from src.db.model import TestUser


class TestMysql(MysqlBase):

    @allure.epic('Awesome test application')
    @allure.feature('DB tests')
    @allure.story('Create user')
    def test_create_user(self):
        create_user = TestUser(
            username="createuser",
            password="1234",
            email="createuser@test.ru"
        )
        self.api_client.create_user(create_user.username, create_user.password, create_user.email)
        found_user = self.mysql.session.query(TestUser) \
            .filter(TestUser.username == create_user.username) \
            .filter(TestUser.password == create_user.password) \
            .filter(TestUser.email == create_user.email).all()
        result = len(found_user) == 1
        self.api_client.delete_user(create_user.username)
        assert result

    @allure.epic('Awesome test application')
    @allure.feature('DB tests')
    @allure.story('Delete user')
    def test_delete_user(self):
        delete_user = TestUser(
            username="deleteuser",
            password="1234",
            email="deleteuser@test.ru"
        )
        self.api_client.create_user(delete_user.username, delete_user.password, delete_user.email)
        self.api_client.delete_user(delete_user.username)
        found_user = self.mysql.session.query(TestUser) \
            .filter(TestUser.username == delete_user.username) \
            .filter(TestUser.password == delete_user.password) \
            .filter(TestUser.email == delete_user.email).all()
        assert len(found_user) == 0

    @allure.epic('Awesome test application')
    @allure.feature('DB tests')
    @allure.story('Block user')
    def test_block_user(self):
        test_user = TestUser(
            username="blockuser1",
            password="1234",
            email="blockuser1@test.ru"
        )
        self.api_client.create_user(test_user.username, test_user.password, test_user.email)
        self.api_client.block_user(test_user.username)
        found_user = self.mysql.session.query(TestUser) \
            .filter(TestUser.username == test_user.username) \
            .filter(TestUser.password == test_user.password) \
            .filter(TestUser.email == test_user.email).first()
        assert found_user.access == 0

    @allure.epic('Awesome test application')
    @allure.feature('DB tests')
    @allure.story('Accept user')
    def test_accept_user(self):
        accept_user = TestUser(
            username="acceptuser",
            password="1234",
            email="acceptusere@test.ru"
        )
        self.api_client.create_user(accept_user.username, accept_user.password, accept_user.email)
        self.api_client.block_user(accept_user.username)
        self.api_client.accept_user(accept_user.username)
        found_user = self.mysql.session.query(TestUser) \
            .filter(TestUser.username == accept_user.username) \
            .filter(TestUser.password == accept_user.password) \
            .filter(TestUser.email == accept_user.email).first()
        assert found_user.access == 1

    @allure.epic('Awesome test application')
    @allure.feature('DB tests')
    @allure.story('Block user')
    def test_block_blocked_user(self):
        block_user = TestUser(
            username="blockuser2",
            password="1234",
            email="blockuser2@test.ru"
        )
        self.api_client.create_user(block_user.username, block_user.password, block_user.email)
        self.api_client.block_user(block_user.username)
        self.api_client.block_user(block_user.username)
        found_user = self.mysql.session.query(TestUser) \
            .filter(TestUser.username == block_user.username) \
            .filter(TestUser.password == block_user.password) \
            .filter(TestUser.email == block_user.email).first()
        assert found_user.access == 0
