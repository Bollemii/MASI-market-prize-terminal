from abc import ABC, abstractmethod
from datetime import datetime

from src.dataaccess.entities.tombola_entity import TombolaEntity
from src.models.tombola_model import TombolaModel
from src.models.prize_model import PrizeModel


class ITombolaDAO(ABC):
    """Interface for TombolaDao"""

    @abstractmethod
    def convert_tombola_entity_to_tombola_model(
        self, entity: TombolaEntity
    ) -> TombolaModel:
        """Convert tombola entity to tombola model"""

    @abstractmethod
    def get_current_tombola(self) -> TombolaModel | None:
        """Get current tombola"""

    @abstractmethod
    def create(self, start_date: datetime, end_date: datetime) -> TombolaModel:
        """Create tombola"""

    @abstractmethod
    def create_tombola_with_prize(
        self,
        start_date: datetime,
        end_date: datetime,
        prizes: list[PrizeModel],
        nb_tickets: int,
    ) -> TombolaModel:
        """Create tombola with prize"""

    @abstractmethod
    def are_tombolas_in_dates_range(
        self, start_date: datetime, end_date: datetime
    ) -> bool:
        """Check if there are tombola in dates range"""
