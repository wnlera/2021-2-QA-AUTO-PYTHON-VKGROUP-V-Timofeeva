import pytest

from client import MysqlORMClient
from statsORM import StatsORM


class MysqlBase:
    @pytest.fixture(scope='function', autouse=True)
    def setup(self, mysql_orm_client):
        self.mysql: MysqlORMClient = mysql_orm_client
        self.stats_orm: StatsORM = StatsORM(self.mysql)

