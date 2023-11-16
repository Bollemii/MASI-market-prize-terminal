import pytest

from src.dataaccess.dao.city_dao import CityDAO
from src.dataaccess.entity.city_entity import CityEntity


class TestPrizeDAO:
    @pytest.fixture(scope="function", autouse=True, name="temp_folder")
    def create_temporary_testfolder(
        self, tmp_path_factory: pytest.TempPathFactory
    ) -> str:
        base_path = "test_prize_dao"
        return str(tmp_path_factory.mktemp(base_path, True))

    def test_converter_entity_to_model(self, temp_folder):
        city_dao = CityDAO(temp_folder)

        entity = CityEntity(1, "name", "postal_code")

        model = city_dao.convert_city_entity_to_city_model(entity)

        assert model.id == entity.id
        assert model.name == entity.name
        assert model.postal_code == entity.postal_code
