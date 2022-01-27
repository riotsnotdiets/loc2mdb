from loc2mdb.config import Config
import os
import sqlite3
from sqlalchemy import create_engine, Column, Integer, String
from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.declarative import declarative_base

Base = declarative_base()

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

    def __repr__(self):
        return f'Person {self.vorname} {self.nachname}'


class Id(Base):
    __tablename__ = 'ids'
    abgwatch_id = Column(Integer, primary_key=True, autoincrement=False)
    mdb_id = Column(Integer)


def create_db():
    debug = Config.get('DEBUG')
    print('*** DEBUG *** :',debug)
    sqlite_file_name = Config.get('SQLITE_FILE_NAME')
    file = os.path.join(os.path.split(os.path.abspath(os.path.dirname(__file__)))[0], 'loc2mdb','data', sqlite_file_name)

    # check if file exists
    print(file)
    if os.path.isfile(file):
        return {'error': True, 'error_msg_debug': 'cant create new sqlite-db when the file already exists, please rename, remove or delete first'}

    if debug:
        engine = create_engine(f'sqlite:///{file}', echo=True)  # log all SQL commands
    else:
        engine = create_engine(f'sqlite:///{file}', echo=False)

    Session = sessionmaker(bind=engine)
    session = Session()

    Base.metadata.create_all(engine, checkfirst=True)
    session.commit()



#print(create_db())