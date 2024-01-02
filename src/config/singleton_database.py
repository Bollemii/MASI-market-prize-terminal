import sqlite3

from src.config import db


class SingletonDatabase:
    _instances = {}

    def __init__(self, base_path: str):
        self.connection = sqlite3.connect(f"{base_path}/database.sqlite")
        self.cursor = self.connection.cursor()

    def __new__(cls, base_path: str):
        if base_path not in cls._instances:
            cls._instances[base_path] = super(SingletonDatabase, cls).__new__(cls)
        return cls._instances[base_path]

    def create_database(self):
        all_tables = self.cursor.execute(
            "SELECT name FROM sqlite_master WHERE type='table';"
        ).fetchall()
        if len(all_tables) == 0:
            try:
                self.cursor.execute("begin")
                self.cursor.execute(db.user_table_ddl)
                self.cursor.execute(db.city_table_ddl)
                self.cursor.execute(db.ticket_table_ddl)
                self.cursor.execute(db.tombola_table_ddl)
                self.cursor.execute(db.tombola_prize_table_ddl)
                self.cursor.execute(db.prize_table_ddl)
                self.cursor.execute("commit")
            except Exception as e:
                self.cursor.execute("rollback")
                raise e

    def get_connection(self):
        return self.connection

    def get_cursor(self):
        return self.cursor
