from abc import ABC, abstractmethod

from src.models.user_model import UserModel


class IUpdateEmailAccountController(ABC):
    """Interface for UpdateEmailAccountController"""

    @abstractmethod
    def update_email(self, id: int, email: str) -> UserModel:
        """Update the user email"""
