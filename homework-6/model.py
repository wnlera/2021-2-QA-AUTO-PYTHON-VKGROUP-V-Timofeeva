from sqlalchemy import Column, Integer, String, Float
from sqlalchemy.ext.declarative import declarative_base

Base = declarative_base()


class RequestCount(Base):
    __tablename__ = 'RequestCount'
    __table_args__ = {'mysql_charset': 'utf8'}

    def __repr__(self):
        return f"<RequestCount(" \
               f"id='{self.id}'," \
               f"count='{self.count}', " \
               f")>"

    id = Column(Integer, primary_key=True, autoincrement=True)
    count = Column(Integer, nullable=False)


class CountWithTypes(Base):
    __tablename__ = 'CountWithTypes'
    __table_args__ = {'mysql_charset': 'utf8'}

    def __repr__(self):
        return f"<CountWithType(" \
               f"id='{self.id}'," \
               f"method='{self.method}'," \
               f"count='{self.count}', " \
               f")>"

    id = Column(Integer, primary_key=True, autoincrement=True)
    method = Column(String(8), nullable=False)
    count = Column(Integer, nullable=False)


class FrequentRequests(Base):
    __tablename__ = 'FrequentRequests'
    __table_args__ = {'mysql_charset': 'utf8'}

    def __repr__(self):
        return f"<FrequentRequests(" \
               f"id='{self.id}'," \
               f"url='{self.url}'," \
               f"count='{self.count}', " \
               f")>"

    id = Column(Integer, primary_key=True, autoincrement=True)
    url = Column(String(50), nullable=False)
    count = Column(Integer, nullable=False)


class ClientErrorRequests(Base):
    __tablename__ = 'ClientErrorRequests'
    __table_args__ = {'mysql_charset': 'utf8'}

    def __repr__(self):
        return f"<ClientErrorRequests(" \
               f"id='{self.id}'," \
               f"url='{self.url}'," \
               f"status='{self.status}',"\
               f"size='{self.size}'," \
               f"ip='{self.ip}'," \
               f")>"

    id = Column(Integer, primary_key=True, autoincrement=True)
    url = Column(String(120), nullable=False)
    status = Column(Integer, nullable=False)
    size = Column(Float, nullable=False)
    ip = Column(String(20), nullable=False)


class ServerErrorRequests(Base):
    __tablename__ = 'ServerErrorRequests'
    __table_args__ = {'mysql_charset': 'utf8'}

    def __repr__(self):
        return f"<FrequentRequests(" \
               f"id='{self.id}'," \
               f"ip='{self.ip}'," \
               f"count='{self.count}', " \
               f")>"

    id = Column(Integer, primary_key=True, autoincrement=True)
    ip = Column(String(20), nullable=False)
    count = Column(Integer, nullable=False)
