import pytest

from client import MysqlORMClient


def pytest_configure(config):
    mysql_orm_client = MysqlORMClient(user="root", password="pass", db_name="TEST_SQL")
    if not hasattr(config, "workerinput"):
        mysql_orm_client.recreate_db()
    mysql_orm_client.connect(db_created=True)
    if not hasattr(config, "workerinput"):
        mysql_orm_client.create_request_count()
        mysql_orm_client.create_count_with_types()
        mysql_orm_client.create_frequent_requests()
        mysql_orm_client.create_client_error_requests()
        mysql_orm_client.create_server_error_requests()

    config.mysql_orm_client = mysql_orm_client


@pytest.fixture(scope='session')
def mysql_orm_client(request) -> MysqlORMClient:
    client = request.config.mysql_orm_client
    yield client
    client.connection.close()


def pytest_addoption(parser):
    parser.addoption(
        "--file", action="store", default=r"C:\Users\Valery\Downloads\access.log", help="Укажите путь до лог файла"
    )


@pytest.fixture()
def file_log(request):
    return request.config.getoption('--file')
