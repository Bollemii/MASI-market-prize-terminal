from src.dataaccess.entity.city_entity import City as CityEntity
from src.dataaccess.repository.city_repository import CityRepository
from src.model.city import City


class CityDAO:
    def __init__(self, base_path: str):
        self.city_repository = CityRepository(base_path)

    def convert_city_entity_to_city_model(self, entity: CityEntity) -> City:
        return City(
            id=entity.id,
            name=entity.name,
            postal_code=entity.postal_code,
        )
