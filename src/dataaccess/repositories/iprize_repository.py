from abc import ABC, abstractmethod

from src.dataaccess.entities.prize_entity import PrizeEntity


class IPrizeRepository(ABC):
    """Interface for PrizeRepository"""

    @abstractmethod
    def get_by_id(self, id: int) -> PrizeEntity | None:
        """Get prize by id"""

    @abstractmethod
    def get_by_tombola_id(self, tombola_id: int) -> list[PrizeEntity]:
        """Get prize by tombola id"""

    @abstractmethod
    def prize_won(self, id: int) -> PrizeEntity:
        """Prize won"""

    @abstractmethod
    def create_prize_item(self, description: str) -> int:
        """Create prize item"""

    @abstractmethod
    def create(self, tombola_id: int, description: str, quantity: int) -> PrizeEntity:
        """Create prize"""
