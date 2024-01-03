from abc import ABC, abstractmethod

from src.dataaccess.entities.user_entity import UserEntity


class IUserRepository(ABC):
    """Interface for UserRepository"""

    @abstractmethod
    def get_by_id(self, id: int) -> UserEntity | None:
        """Get user by id"""

    @abstractmethod
    def get_by_email(self, email: str) -> UserEntity | None:
        """Get user by email"""

    @abstractmethod
    def update_email(self, id: int, email: str) -> UserEntity:
        """Update the user email"""

    @abstractmethod
    def update_password(self, id: int, password: str) -> UserEntity:
        """Update the user password"""

    @abstractmethod
    def connection(self, email: str, password: str) -> UserEntity | None:
        """Connect a user"""

    @abstractmethod
    def register(
        self, email: str, password: str, city_name: str, postal_code: str
    ) -> UserEntity:
        """Register a user"""

    @abstractmethod
    def check_tenant_password(self, password: str) -> bool:
        """Check if the tenant password is correct"""
