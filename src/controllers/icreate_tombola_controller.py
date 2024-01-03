from abc import ABC, abstractmethod
from datetime import datetime

from src.models.prize_model import PrizeModel
from src.models.tombola_model import TombolaModel


class ICreateTombolaController(ABC):
    """Interface for CreateTombolaController"""

    @abstractmethod
    def create_tombola(
        self,
        start_date: datetime,
        end_date: datetime,
        prizes: list[PrizeModel],
        nb_tickets: int,
    ) -> TombolaModel:
        """Create a complete tombola with prizes and tickets"""
