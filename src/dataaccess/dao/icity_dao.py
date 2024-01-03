from abc import ABC, abstractmethod

from src.dataaccess.entities.city_entity import CityEntity
from src.models.city_model import CityModel


class ICityDAO(ABC):
    """Interface for CityDao"""

    @abstractmethod
    def convert_city_entity_to_city_model(self, entity: CityEntity) -> CityModel:
        """Convert city entity to city model"""
