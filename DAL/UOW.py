from peewee import *

from Helper.Singleton import Singleton


# SQLite database using WAL journal mode and 64MB cache.

class UOW(metaclass=Singleton):
    db = SqliteDatabase('app.db', pragmas={
        'journal_mode': 'wal',
        'cache_size': -1024 * 64})

    def __init__(self):
        print("load db")


class BaseModel(Model):
    class Meta:
        database = UOW.db
