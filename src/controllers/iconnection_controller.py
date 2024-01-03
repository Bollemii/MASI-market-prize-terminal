from abc import ABC, abstractmethod

from src.models.user_model import UserModel


class IConnectionController(ABC):
    """Interface for ConnectionController"""

    @abstractmethod
    def connection(self, email: str, password: str) -> UserModel:
        """Connect a user"""
