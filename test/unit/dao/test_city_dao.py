import pytest

from src.dataaccess.dao.city_dao import CityDAO
from src.dataaccess.entity.city_entity import CityEntity
from src.dataaccess.repository.city_repository import CityRepository


class TestCity:
    @pytest.fixture(scope="function", autouse=True, name="temp_folder")
    def create_temporary_testfolder(
        self, tmp_path_factory: pytest.TempPathFactory
    ) -> str:
        base_path = "test_city_dao"
        return str(tmp_path_factory.mktemp(base_path, True))

    @pytest.fixture(scope="function", autouse=True, name="city_dao")
    def create_city_dao(self, temp_folder: str) -> CityDAO:
        city_repository = CityRepository(temp_folder)
        return CityDAO(city_repository)

    def test_entity_model_city_convertion(self, city_dao: CityDAO):
        entity = CityEntity(id=1, name="name", postal_code="postal_code")

        city = city_dao.convert_city_entity_to_city_model(entity)

        assert city.id == entity.id
        assert city.name == entity.name
        assert city.postal_code == entity.postal_code
