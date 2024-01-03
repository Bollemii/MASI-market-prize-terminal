from abc import ABC, abstractmethod

from src.dataaccess.entities.user_entity import UserEntity


class IUserRepository(ABC):
    """Interface for UserRepository"""

    @abstractmethod
    def get_by_id(self, id: int) -> UserEntity | None:
        """Get user by id"""

    @abstractmethod
    def update(self, id: int, email: str, password: str) -> UserEntity:
        """Update a user"""

    @abstractmethod
    def connection(self, email: str, password: str) -> UserEntity | None:
        """Connect a user"""

    @abstractmethod
    def register(
        self, email: str, password: str, city_name: str, postal_code: str
    ) -> UserEntity:
        """Register a user"""
