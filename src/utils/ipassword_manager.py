from abc import ABC, abstractmethod


class IPasswordManager(ABC):
    """Interface for PasswordManager"""

    @abstractmethod
    def encrypt_password(self, password: str) -> str:
        """Encrypt password"""

    @abstractmethod
    def check_password(self, password: str, hashed_password: str | bytes) -> bool:
        """Check password"""
