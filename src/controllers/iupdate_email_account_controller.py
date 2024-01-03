from abc import ABC, abstractmethod

from src.models.user_model import UserModel


class IUpdateEmailAccountController(ABC):
    """Interface for UpdateEmailAccountController"""

    @abstractmethod
    def update_email(self, user: UserModel, email: str) -> UserModel:
        """Update the user email"""
