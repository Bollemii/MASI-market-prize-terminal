import pytest

from src.config.singleton_database import SingletonDatabase


class TestSingletonDatabase:
    """Test singleton database"""

    @pytest.fixture(scope="function", autouse=True, name="temp_folder")
    def create_temporary_testfolder(
        self, tmp_path_factory: pytest.TempPathFactory
    ) -> str:
        base_path = "test_user_repository"
        return str(tmp_path_factory.mktemp(base_path, True))

    @pytest.fixture(scope="function", autouse=True, name="temp_folder_2")
    def create_temporary_testfolder_copy(
        self, tmp_path_factory: pytest.TempPathFactory
    ) -> str:
        base_path = "test_user_repository"
        return str(tmp_path_factory.mktemp(base_path, True))

    def test_init(self, temp_folder):
        """Test init"""
        singleton_database = SingletonDatabase(temp_folder)

        assert singleton_database.connection is not None
        assert singleton_database.cursor is not None

    def test_get_connection(self, temp_folder):
        """Test get connection"""
        singleton_database = SingletonDatabase(temp_folder)

        assert singleton_database.get_connection() is not None

    def test_get_cursor(self, temp_folder):
        """Test get cursor"""
        singleton_database = SingletonDatabase(temp_folder)

        assert singleton_database.get_cursor() is not None

    def test_singleton(self, temp_folder):
        """Test singleton"""
        singleton_database = SingletonDatabase(temp_folder)
        singleton_database_2 = SingletonDatabase(temp_folder)

        assert singleton_database == singleton_database_2
        assert singleton_database.connection == singleton_database_2.connection
        assert singleton_database.cursor == singleton_database_2.cursor

    def test_singleton_different_path(self, temp_folder, temp_folder_2):
        """Test singleton different path"""
        singleton_database = SingletonDatabase(temp_folder)
        singleton_database_2 = SingletonDatabase(temp_folder_2)

        assert singleton_database != singleton_database_2
        assert singleton_database.connection != singleton_database_2.connection
        assert singleton_database.cursor != singleton_database_2.cursor
