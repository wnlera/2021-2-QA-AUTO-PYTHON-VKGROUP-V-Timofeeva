import sqlalchemy
from sqlalchemy import inspect
from sqlalchemy.orm import sessionmaker

from model import Base


class MysqlORMClient:

    def __init__(self, user, password, db_name, host='127.0.0.1', port=3306):
        self.user = user
        self.password = password
        self.db_name = db_name

        self.host = host
        self.port = port

        self.engine = None
        self.connection = None
        self.session = None

    def connect(self, db_created=True):
        db = self.db_name if db_created else ''
        url = f'mysql+pymysql://{self.user}:{self.password}@{self.host}:{self.port}/{db}'

        self.engine = sqlalchemy.create_engine(url, encoding='utf8')
        self.connection = self.engine.connect()

        sm = sessionmaker(bind=self.connection.engine)  # session creation wrapper
        self.session = sm()

    def recreate_db(self):
        self.connect(db_created=False)

        # these two requests we need to do in ras SQL syntax
        self.execute_query(f'DROP database if exists {self.db_name}', fetch=False)
        self.execute_query(f'CREATE database {self.db_name}', fetch=False)

        self.connection.close()

    def execute_query(self, query, fetch=True):
        res = self.connection.execute(query)
        if fetch:
            return res.fetchall()

    def create_request_count(self):
        if not inspect(self.engine).has_table('RequestCount'):
            Base.metadata.tables['RequestCount'].create(self.engine)

    def create_count_with_types(self):
        if not inspect(self.engine).has_table('CountWithTypes'):
            Base.metadata.tables['CountWithTypes'].create(self.engine)

    def create_frequent_requests(self):
        if not inspect(self.engine).has_table('FrequentRequests'):
            Base.metadata.tables['FrequentRequests'].create(self.engine)

    def create_client_error_requests(self):
        if not inspect(self.engine).has_table('ClientErrorRequests'):
            Base.metadata.tables['ClientErrorRequests'].create(self.engine)

    def create_server_error_requests(self):
        if not inspect(self.engine).has_table('ServerErrorRequests'):
            Base.metadata.tables['ServerErrorRequests'].create(self.engine)
