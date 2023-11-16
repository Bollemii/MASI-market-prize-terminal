import pytest
from datetime import datetime

from src.dataaccess.dao.tombola_dao import TombolaDAO
from src.dataaccess.entity.tombola_entity import TombolaEntity


class TestTombolaDAO:
    @pytest.fixture(scope="function", autouse=True, name="temp_folder")
    def create_temporary_testfolder(
        self, tmp_path_factory: pytest.TempPathFactory
    ) -> str:
        base_path = "test_tombola_dao"
        return str(tmp_path_factory.mktemp(base_path, True))

    def test_converter_entity_to_model(self, temp_folder):
        tombola_dao = TombolaDAO(temp_folder)

        entity = TombolaEntity(
            1,
            datetime.fromisoformat("2000-01-01 00:00:00"),
            datetime.fromisoformat("9999-01-01 00:00:00"),
        )

        model = tombola_dao.convert_tombola_entity_to_tombola_model(entity)

        assert model.id == entity.id
        assert model.start_date == entity.start_date
        assert model.end_date == entity.end_date
