import sqlite3

class UOW:
    conn = sqlite3.connect('test.db')
