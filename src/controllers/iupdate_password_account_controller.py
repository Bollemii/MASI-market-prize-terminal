from abc import ABC, abstractmethod

from src.models.user_model import UserModel


class IUpdatePasswordAccountController(ABC):
    """Interface for UpdatePasswordAccountController"""

    @abstractmethod
    def update_password(
        self, user: UserModel, password: str, confirm_password: str
    ) -> UserModel:
        """Update the user password"""
