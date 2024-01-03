from abc import ABC, abstractmethod

from src.models.tombola_model import TombolaModel


class IGetCurrentTombolaController(ABC):
    """Interface for get current tombola"""

    @abstractmethod
    def get_current_tombola(self) -> TombolaModel | None:
        """Get current tombola"""
