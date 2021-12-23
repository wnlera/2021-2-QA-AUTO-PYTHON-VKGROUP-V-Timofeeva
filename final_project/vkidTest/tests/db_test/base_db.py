import pytest

from src.db.client import MysqlORMClient
from src.api.client import ApiClient


class MysqlBase:
    @pytest.fixture(scope='function', autouse=True)
    def setup(self, mysql_orm_client, logger, api_client):
        self.logger = logger
        self.mysql: MysqlORMClient = mysql_orm_client
        self.api_client: ApiClient = api_client