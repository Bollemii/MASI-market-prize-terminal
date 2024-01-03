from abc import ABC, abstractmethod

from src.dataaccess.entities.user_entity import UserEntity
from src.models.user_model import UserModel


class IUserDAO(ABC):
    """Interface for UserDao"""

    @abstractmethod
    def convert_user_entity_to_user_model(self, entity: UserEntity) -> UserModel:
        """Convert user entity to user model"""

    @abstractmethod
    def connection(self, email: str, password: str) -> UserModel:
        """Connection"""

    @abstractmethod
    def register(
        self, email: str, password: str, city_name: str, postal_code: str
    ) -> UserModel:
        """Register user"""

    @abstractmethod
    def update(
        self, user: UserModel, email: str | None = None, password: str | None = None
    ) -> UserModel:
        """Update user"""
