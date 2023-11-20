import pytest
from datetime import datetime

from src.dataaccess.dao.tombola_dao import TombolaDAO
from src.model.tombola_model import TombolaModel


class TestTombolaDAO:
    @pytest.fixture(scope="function", autouse=True, name="temp_folder")
    def create_temporary_testfolder(
        self, tmp_path_factory: pytest.TempPathFactory
    ) -> str:
        base_path = "test_tombola_dao"
        return str(tmp_path_factory.mktemp(base_path, True))

    def test_tombola_created(self, temp_folder):
        tombola_dao = TombolaDAO(temp_folder)
        tombola = TombolaModel(
            1, datetime.fromisoformat("2000-01-01 00:00:00"), datetime.now()
        )
        tombola = tombola_dao.create(tombola.start_date, tombola.end_date)

        assert tombola is not None
        assert tombola.start_date == tombola.start_date
        assert tombola.end_date == tombola.end_date

    def test_get_current_tombola(self, temp_folder):
        tombola_dao = TombolaDAO(temp_folder)
        tombola = TombolaModel(
            1,
            datetime.fromisoformat("2000-01-01 00:00:00"),
            datetime.fromisoformat("9999-01-01 00:00:00"),
        )
        tombola = tombola_dao.create(tombola.start_date, tombola.end_date)

        current_tombola = tombola_dao.get_current_tombola()

        assert current_tombola is not None
        assert current_tombola.id == tombola.id
        assert current_tombola.start_date == tombola.start_date
        assert current_tombola.end_date == tombola.end_date
