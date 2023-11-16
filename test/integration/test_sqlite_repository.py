import pytest
import sqlite3

from src.dataaccess.repository.common.sqlite_repository import SqliteRepository


class TestSqliteRepository:
    """Test sqlite repository"""

    @pytest.fixture(scope="function", autouse=True, name="temp_folder")
    def create_temporary_testfolder(
        self, tmp_path_factory: pytest.TempPathFactory
    ) -> str:
        base_path = "test_user_repository"
        return str(tmp_path_factory.mktemp(base_path, True))

    @pytest.fixture(scope="function", autouse=True, name="city_table")
    def create_city_table(self, temp_folder):
        connection = sqlite3.connect(temp_folder + "/database.sqlite")
        cursor = connection.cursor()
        cursor.execute(
            """
            CREATE TABLE IF NOT EXISTS city (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                name TEXT NOT NULL,
                postal_code TEXT NOT NULL
            );
        """
        )
        connection.commit()

    def test_init(self, temp_folder):
        """Test init"""
        sqlite_repository = SqliteRepository(temp_folder)

        assert sqlite_repository.base_path == temp_folder

    def test_query_cleaner(self, temp_folder):
        """Test query cleaner"""
        sqlite_repository = SqliteRepository(temp_folder)
        query = """
            SELECT * FROM user\n WHERE email               = ? AND password  \t = ?
        """
        query_cleaned = sqlite_repository.query_cleaner(query)

        assert query_cleaned == "SELECT * FROM user WHERE email = ? AND password = ?"

    def test_execute_statement_returning(self, temp_folder, city_table):
        """Test execute statement returning"""
        sqlite_repository = SqliteRepository(temp_folder)

        result = sqlite_repository.execute_statement(
            "INSERT INTO city (name, postal_code) VALUES (?, ?)", ("City", "1111")
        )

        assert result == [(1, "City", "1111")]

    def test_execute_statement_not_returning(self, temp_folder, city_table):
        """Test execute statement not returning"""
        sqlite_repository = SqliteRepository(temp_folder)

        result = sqlite_repository.execute_statement(
            "DELETE FROM city WHERE id = ?", (1,)
        )

        assert result is None

    def test_multiple_execute_statement(self, temp_folder, city_table):
        """Test multiple execute statement"""
        sqlite_repository = SqliteRepository(temp_folder)

        sqlite_repository.execute_statement(
            "INSERT INTO city (name, postal_code) VALUES (?, ?)", ("City", "1111")
        )
        sqlite_repository.execute_statement(
            "INSERT INTO city (name, postal_code) VALUES (?, ?)", ("City2", "1112")
        )
        result = sqlite_repository.execute_query("SELECT * FROM city")

        assert result == [(1, "City", "1111"), (2, "City2", "1112")]

    def test_execute_query(self, temp_folder, city_table):
        """Test execute query"""
        sqlite_repository = SqliteRepository(temp_folder)

        sqlite_repository.execute_statement(
            "INSERT INTO city (name, postal_code) VALUES (?, ?)", ("City", "1111")
        )
        result = sqlite_repository.execute_query("SELECT * FROM city")

        assert result == [(1, "City", "1111")]
