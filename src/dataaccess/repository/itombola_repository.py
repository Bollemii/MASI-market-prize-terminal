from abc import ABC, abstractmethod
from datetime import datetime

from src.dataaccess.entity.tombola_entity import TombolaEntity


class ITombolaRepository(ABC):
    """Interface for TombolaRepository"""

    @abstractmethod
    def get_by_id(self, id: int) -> TombolaEntity | None:
        """Get tombola by id"""

    @abstractmethod
    def get_tombola_by_date(self, current_date: datetime) -> TombolaEntity | None:
        """Get tombola by date"""

    @abstractmethod
    def create(self, start_date: datetime, end_date: datetime) -> TombolaEntity:
        """Create tombola"""
