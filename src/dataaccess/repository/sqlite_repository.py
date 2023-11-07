from src.config.db import SingletonDatabase


class SqliteRepository:
    def __init__(self, base_path: str):
        self.base_path = base_path

    def execute_statement(self, statement: str, params: tuple = ()) -> list | None:
        self.db_cursor = SingletonDatabase(self.base_path).cursor

        if not statement.startswith("DELETE"):
            statement += " RETURNING *"

        self.db_cursor.execute(statement, params)

        if statement.startswith("INSERT"):
            return [self.db_cursor.fetchone()]
        elif statement.startswith("UPDATE"):
            return self.db_cursor.fetchall()
        return None

    def execute_query(self, query: str, params: tuple = ()) -> list:
        self.db_cursor = SingletonDatabase(self.base_path).cursor

        self.db_cursor.execute(query, params)
        return self.db_cursor.fetchall()
