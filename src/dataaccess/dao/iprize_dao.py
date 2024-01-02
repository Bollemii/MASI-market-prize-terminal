from abc import ABC, abstractmethod

from src.dataaccess.entity.prize_entity import PrizeEntity
from src.model.prize_model import PrizeModel


class IPrizeDAO(ABC):
    """Interface for PrizeDao"""

    @abstractmethod
    def convert_prize_entity_to_prize_model(self, entity: PrizeEntity) -> PrizeModel:
        """Convert prize entity to prize model"""

    @abstractmethod
    def prize_won(self, prize: PrizeModel) -> PrizeModel:
        """Prize won"""

    @abstractmethod
    def create(self, tombola_id: int, description: str, quantity: int) -> PrizeModel:
        """Create prize"""

    @abstractmethod
    def get_by_tombola(self, tombola_id: int) -> list[PrizeModel]:
        """Get prizes by tombola id"""
