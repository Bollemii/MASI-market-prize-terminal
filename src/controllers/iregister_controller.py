from abc import ABC, abstractmethod

from src.model.user_model import UserModel


class IRegisterController(ABC):
    """Interface for RegisterController"""

    @abstractmethod
    def register(
        self,
        email: str,
        password: str,
        confirm_password: str,
        city_name: str,
        postal_code: str,
    ) -> UserModel:
        """Register a user"""
