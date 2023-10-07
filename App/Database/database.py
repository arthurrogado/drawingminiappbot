from telebot import TeleBot
import sqlite3
from datetime import datetime as dt

from ..Config.config import DB_NAME
from ..Utils.constants import CLOUD_ID

class DB:
    def __init__(self, bot: TeleBot = None):
        self.bot = bot
        # Here you can set a connection to a database likely on any relational database management system (RDBMS) like MySQL, PostgreSQL, SQLite, etc.
        self.conn = sqlite3.connect(DB_NAME, check_same_thread=False)
        self.cursor = self.conn.cursor()

    def send_backup(self):
        try:
            self.bot.send_document(CLOUD_ID, open(DB_NAME, 'rb'), caption='Backup database')
        except Exception as e:
            # print(e)
            pass

    # Generic methods for CRUD

    def insert(self, table: str, columns: list, values: list):
        # Example: insert('users', ['userid', 'lang'], [userid, lang])
        # Example multiple values: insert('users', ['userid', 'lang'], [[userid1, lang1], [userid2, lang2]])
        
        sql = f'INSERT INTO {table} ({",".join(columns)}) VALUES ({",".join(["?" for _ in values])})'
        self.cursor.execute(sql, values)
        self.conn.commit()

        self.send_backup()

        # returns the row id of the cursor object, or None if no row was inserted or an error occurred.
        return self.cursor.lastrowid
    
    # select with return as dict
    def select(self, table: str, columns: list, where = None):
        # Example: select('users', ['userid', 'lang'], 'userid = ?', [userid])
        # Example multiple where: select('users', ['userid', 'lang'], "userid = '850446631' AND lang = 'pt' ")
        # Example get all from table: select('users', ['*'])
        sql = f"""
            SELECT {",".join(columns)}
            FROM {table}
            {f' WHERE {where}' if where else ''}
        """
        self.cursor.execute(sql)
        rows = self.cursor.fetchall()
        return [dict(zip([key[0] for key in self.cursor.description], row)) for row in rows]
    
    def update(self, table: str, columns: list, values: list, where: str = None):
        # Example: update('users', ['lang'], 'userid = ?', [userid])
        # Example multiple where: update('users', ['lang'], f"userid = {userid} AND lang = {lang}")        

        self.cursor.execute(f'UPDATE {table} SET {",".join([f"{column} = ?" for column in columns])}' + (f' WHERE {where}' if where else ''), values)
        self.conn.commit()
        self.send_backup()
        # return True if at least one row was modified, False otherwise.
        return self.cursor.rowcount > 0
        

    def delete(self, table: str, where: str = None, values: list = None):
        # Example: delete('users', 'userid = ?', [userid])
        # Example multiple where: delete('users', 'userid = ? AND lang = ?', [userid, lang])
        self.cursor.execute(f'DELETE FROM {table}' + (f' WHERE {where}' if where else ''), values)
        self.conn.commit()
        self.send_backup()
        return self.cursor.rowcount > 0