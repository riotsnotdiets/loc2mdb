from loc2mdb.config import Config
import os
import sqlite3
from sqlalchemy import create_engine, Column, Integer, String, DateTime
from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.declarative import declarative_base

Base = declarative_base()
file = os.path.join(os.path.split(os.path.abspath(os.path.dirname(__file__)))[0], 'loc2mdb','data', Config.get('SQLITE_FILE_NAME'))

# connect to the engine, doesnt care if file exists
debug = Config.get('DEBUG')
if debug:
    engine = create_engine(f'sqlite:///{file}', echo=True)  # log all commands
else:
    engine = create_engine(f'sqlite:///{file}', echo=False)

# we can now construct a Session() without needing to pass the engine each time
Session = sessionmaker(engine, future=True)  # https://docs.sqlalchemy.org/en/14/orm/session_basics.html#querying-2-0-style


class Person(Base):
    __tablename__ = 'persons'
    id = Column(Integer, primary_key=True)
    einzug_ueber = Column(String)
    abgwatch_api = Column(String)
    abgwatch_url = Column(String)
    abgwatch_id = Column(String)
    vorname = Column(String)
    nachname = Column(String)
    partei_fraktion = Column(String)
    partei_name = Column(String)
    last_update = Column(DateTime(timezone=True))

    def __repr__(self):
        return f'Person {self.vorname} {self.nachname}'


class Constituency(Base):
    __tablename__ = 'constituencies'
    id = Column(Integer, primary_key=True, autoincrement=False)
    wahlkreis_id = Column(Integer)
    jahr = Column(Integer)
    label = Column(String)
    name = Column(String)
    abgwatch_api = Column(String)


class Id(Base):
    __tablename__ = 'ids'
    abgwatch_id = Column(Integer, primary_key=True, autoincrement=False)
    mdb_id = Column(Integer)


def create_db():
    # check if file exists
    file = os.path.join(os.path.split(os.path.abspath(os.path.dirname(__file__)))[0], 'loc2mdb','data', Config.get('SQLITE_FILE_NAME'))
    if os.path.isfile(file):
        return {'error': True, 'error_msg_debug': 'cant create db, database file already exists'}

    with Session(engine) as session:
        Base.metadata.create_all(engine, checkfirst=True)
        session.commit()

