import sqlite3

from src.config.isingleton_database import ISingletonDatabase


class SingletonDatabase(ISingletonDatabase):
    _instances = {}

    def __init__(self, base_path: str):
        self.connection = sqlite3.connect(f"{base_path}/database.sqlite")
        self.cursor = self.connection.cursor()

    def __new__(cls, base_path: str):
        if base_path not in cls._instances:
            cls._instances[base_path] = super(SingletonDatabase, cls).__new__(cls)
        return cls._instances[base_path]

    def get_connection(self):
        return self.connection

    def get_cursor(self):
        return self.cursor
