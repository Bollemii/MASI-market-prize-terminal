from abc import ABC, abstractmethod

from src.model.prize_model import PrizeModel


class IGetTombolaStateController(ABC):
    """Interface for get tombola state controller"""

    @abstractmethod
    def get_tickets_state(self, tombola_id: int) -> tuple[int, int]:
        """Get number of tickets played and remaining of a tombola"""

    @abstractmethod
    def get_prizes_state(self, tombola_id: int) -> list[PrizeModel]:
        """Get number of prizes won and remaining of each prize of a tombola"""
