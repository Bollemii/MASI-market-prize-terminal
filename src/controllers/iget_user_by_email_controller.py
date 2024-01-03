from abc import ABC, abstractmethod

from src.models.user_model import UserModel


class IGetUserByEmailController(ABC):
    """Interface for controllers that get a user by email"""

    @abstractmethod
    def get_by_email(self, email: str) -> UserModel:
        """Get user by email"""
