from abc import ABC, abstractmethod

from src.dataaccess.entity.city_entity import CityEntity


class ICityRepository(ABC):
    """Interface for CityRepository"""

    @abstractmethod
    def get_by_id(self, id: int) -> CityEntity | None:
        """Get city by id"""

    @abstractmethod
    def get_by_name_and_postal_code(
        self, name: str, postal_code: str
    ) -> CityEntity | None:
        """Get city by name and postal code"""

    @abstractmethod
    def create(self, name: str, postal_code: str) -> CityEntity:
        """Create city"""
