from test_sql.base import MysqlBase
from model import RequestCount, CountWithTypes, FrequentRequests, ClientErrorRequests, ServerErrorRequests


class TestMysqlCreate(MysqlBase):
    """
    Структура каждого теста:
    1) Заполнение таблицы
    2) Считывание данных
    3) Проверка длины
    """

    def test_table_request_count(self):
        self.request_count = self.stats_orm.get_requests_count()
        request_count = self.mysql.session.query(RequestCount)
        assert len(request_count.all()) == 1

    def test_table_count_with_types(self):
        self.type_count = self.stats_orm.get_requests_type_count()
        count_with_types = self.mysql.session.query(CountWithTypes)
        assert len(count_with_types.all()) == 5

    def test_table_frequent_requests(self):
        self.frequent_request = self.stats_orm.get_frequent_requests()
        frequent_requests = self.mysql.session.query(FrequentRequests)
        assert len(frequent_requests.all()) == 10

    def test_table_client_error_requests(self):
        self.client_error = self.stats_orm.get_biggest_client_error_requests()
        client_error_requests = self.mysql.session.query(ClientErrorRequests)
        assert len(client_error_requests.all()) == 5

    def test_table_server_error_requests(self):
        self.server_error = self.stats_orm.get_frequent_server_error_requests()
        server_error_requests = self.mysql.session.query(ServerErrorRequests)
        assert len(server_error_requests.all()) == 5


