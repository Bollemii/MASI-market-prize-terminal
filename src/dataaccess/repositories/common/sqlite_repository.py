import re

from src.config.isingleton_database import ISingletonDatabase
from src.config.singleton_database import SingletonDatabase


class SqliteRepository:
    """Repository for Sqlite"""

    def __init__(self, base_path: str):
        self.base_path = base_path

        self.singleton_database: ISingletonDatabase

    def query_cleaner(self, query: str) -> str:
        """Clean query"""
        query = query.strip()
        query = query.replace("\n", " ")
        query = query.replace("\t", " ")
        query = re.sub(" +", " ", query)
        return query

    def execute_create_table(self, statement: str) -> None:
        """Execute create table statement"""
        statement = self.query_cleaner(statement)
        if not statement.startswith("CREATE TABLE"):
            raise Exception("Statement must start with CREATE TABLE")

        self.singleton_database = SingletonDatabase(self.base_path)
        self.db_connection = self.singleton_database.get_connection()
        self.db_cursor = self.singleton_database.get_cursor()

        self.db_cursor.execute(statement)
        self.db_connection.commit()

    def execute_statement(self, statement: str, params: tuple = ()) -> list | None:
        """Execute statement"""
        statement = self.query_cleaner(statement)
        if (
            not statement.startswith("INSERT")
            and not statement.startswith("UPDATE")
            and not statement.startswith("DELETE")
            and not statement.startswith("BEGIN")
            and not statement.startswith("COMMIT")
            and not statement.startswith("ROLLBACK")
        ):
            raise Exception("Statement must start with INSERT, UPDATE or DELETE")

        self.singleton_database = SingletonDatabase(self.base_path)
        self.db_connection = self.singleton_database.get_connection()
        self.db_cursor = self.singleton_database.get_cursor()

        if (
            not statement.startswith("DELETE")
            and not statement.startswith("BEGIN")
            and not statement.startswith("COMMIT")
            and not statement.startswith("ROLLBACK")
        ):
            if statement.endswith(";"):
                statement = statement[:-1]
            statement += " RETURNING *;"

        self.db_cursor.execute(statement, params)

        if statement.startswith("INSERT"):
            result = [self.db_cursor.fetchone()]
        elif statement.startswith("UPDATE"):
            result = self.db_cursor.fetchall()
        else:
            result = None

        self.db_connection.commit()
        return result

    def execute_query(self, query: str, params: tuple = ()) -> list:
        """Execute query and"""
        query = self.query_cleaner(query)
        if not query.startswith("SELECT"):
            raise Exception("Query must start with SELECT")

        self.singleton_database = SingletonDatabase(self.base_path)
        self.db_connection = self.singleton_database.get_connection()
        self.db_cursor = self.singleton_database.get_cursor()

        self.db_cursor.execute(query, params)
        return self.db_cursor.fetchall()
