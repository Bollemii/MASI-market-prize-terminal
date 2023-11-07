from src.dataaccess.entity.city_entity import City as CityEntity
from src.model.city import City


class CityDAO:
    def __init__(self):
        pass

    def convert_city_entity_to_city_model(self, entity: CityEntity) -> City:
        return City(
            id=entity.id,
            name=entity.name,
            postal_code=entity.postal_code,
        )
