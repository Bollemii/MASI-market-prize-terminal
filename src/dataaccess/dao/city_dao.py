from src.dataaccess.entity.city_entity import CityEntity
from src.dataaccess.repository.city_repository import CityRepository
from src.model.city_model import CityModel


class CityDAO:
    def __init__(self, base_path: str):
        self.city_repository = CityRepository(base_path)

    def convert_city_entity_to_city_model(self, entity: CityEntity) -> CityModel:
        return CityModel(
            id=entity.id,
            name=entity.name,
            postal_code=entity.postal_code,
        )
