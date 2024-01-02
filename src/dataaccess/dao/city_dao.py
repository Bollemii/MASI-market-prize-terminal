from src.dataaccess.entity.city_entity import CityEntity
from src.dataaccess.repository.icity_repository import ICityRepository
from src.model.city_model import CityModel


class CityDAO:
    def __init__(self, city_repository: ICityRepository):
        self.city_repository = city_repository

    def _convert_city_entity_to_city_model(self, entity: CityEntity) -> CityModel:
        return CityModel(
            id=entity.id,
            name=entity.name,
            postal_code=entity.postal_code,
        )
