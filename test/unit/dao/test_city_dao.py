import pytest

from src.dataaccess.dao.city_dao import CityDAO
from src.dataaccess.entity.city_entity import CityEntity


class TestCity:
    @pytest.fixture(scope="function", autouse=True, name="temp_folder")
    def create_temporary_testfolder(
        self, tmp_path_factory: pytest.TempPathFactory
    ) -> str:
        base_path = "test_city_repository"
        return str(tmp_path_factory.mktemp(base_path, True))

    def test_entity_model_city_convertion(self, temp_folder):
        entity = CityEntity(id=1, name="name", postal_code="postal_code")
        city = CityDAO(temp_folder).convert_city_entity_to_city_model(entity)
        assert city.id == entity.id
        assert city.name == entity.name
        assert city.postal_code == entity.postal_code
