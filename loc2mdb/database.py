from loc2mdb.config import Config
import os
import sqlite3

from flask_sqlalchemy import SQLAlchemy  # let all the session-stuff in their hands


class Person(db.Model):
    __tablename__ = 'persons'
    id = db.Column(db.Integer, primary_key=True)
    einzug_ueber = db.Column(db.String)
    abgwatch_api = db.Column(db.String)
    abgwatch_url = db.Column(db.String)
    abgwatch_id = db.Column(db.String)
    vorname = db.Column(db.String)
    nachname = db.Column(db.String)
    partei_fraktion = db.Column(db.String)
    partei_name = db.Column(db.String)
    last_update = db.Column(db.DateTime(timezone=True))

    def __repr__(self):
        return f'Person {self.vorname} {self.nachname}'


class Constituency(db.Model):
    __tablename__ = 'constituencies'
    id = db.Column(db.Integer, primary_key=True, autoincrement=False)
    wahlkreis_id = db.Column(db.Integer)
    jahr = db.Column(db.Integer)
    label = db.Column(db.String)
    name = db.Column(db.String)
    abgwatch_api = db.Column(db.String)


class Id(db.Model):
    __tablename__ = 'ids'
    abgwatch_id = db.Column(db.Integer, primary_key=True, autoincrement=False)
    mdb_id = db.Column(db.Integer)


def db_create():
    # check if file exists
    file = os.path.join(os.path.split(os.path.abspath(os.path.dirname(__file__)))[0], 'loc2mdb','data', Config.get('SQLITE_FILE_NAME'))
    if not os.path.isfile(file):
        db.create_all()
    #if os.path.isfile(file):
        #return {'error': True, 'error_msg_debug': 'cant create db, database file already exists'}