from dataaccess.entity.city_entity import City as CityEntity
from models.city import City


def convert_city_entity_to_city_model(entity: CityEntity) -> City:
    return City(
        id=entity.id,
        name=entity.name,
        postal_code=entity.postal_code,
    )
