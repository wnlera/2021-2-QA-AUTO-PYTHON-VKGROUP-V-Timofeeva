from sqlalchemy import Column, Integer, String, DATETIME
from sqlalchemy.ext.declarative import declarative_base

Base = declarative_base()


class TestUser(Base):
    __tablename__ = 'test_users'
    __table_args__ = {'mysql_charset': 'utf8'}

    def __init__(self, username, password, email, access=None, active=None, start_active_time=None):
        self.username = username
        self.password = password
        self.email = email
        self.access = access
        self.active = active
        self.start_active_time = start_active_time

    def __repr__(self):
        return f"<RequestCount(" \
               f"id='{self.id}'," \
               f"username='{self.username}', " \
               f"password='{self.password}', "\
               f"email='{self.email}', " \
               f"access='{self.access}', " \
               f"active='{self.active}', " \
               f")>"

    id = Column(Integer, primary_key=True, autoincrement=True)
    username = Column(String(16), nullable=False, unique=True)
    password = Column(String(255), nullable=False)
    email = Column(String(64), nullable=False, unique=True)
    access = Column(Integer, default=None)
    active = Column(Integer, default=None)
    start_active_time = Column(DATETIME, default=None)

