from src.dataaccess.dao.city_dao import CityDAO
from src.dataaccess.entity.city_entity import City as CityEntity


class TestCity:
    def test_entity_model_city_convertion(self):
        entity = CityEntity(id=1, name="name", postal_code="postal_code")
        city = CityDAO().convert_city_entity_to_city_model(entity)
        assert city.id == entity.id
        assert city.name == entity.name
        assert city.postal_code == entity.postal_code
