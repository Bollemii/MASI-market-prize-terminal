from abc import ABC, abstractmethod


class IIsTenantPasswordController(ABC):
    """Interface for controller for checking if the tenant password is correct"""

    @abstractmethod
    def check_password(self, password: str) -> bool:
        """Check if the tenant password is correct"""
