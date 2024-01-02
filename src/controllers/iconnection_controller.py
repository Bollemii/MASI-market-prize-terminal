from abc import ABC, abstractmethod

from src.model.user_model import UserModel


class IConnectionController(ABC):
    """Interface for ConnectionController"""

    @abstractmethod
    def connection(self, email: str, password: str) -> UserModel:
        """Connect a user"""
