from abc import ABC, abstractmethod
from datetime import datetime

from src.dataaccess.entity.tombola_entity import TombolaEntity


class ITombolaRepository(ABC):
    @abstractmethod
    def get_by_id(self, id: int) -> TombolaEntity | None:
        """Get tombola by id"""

    @abstractmethod
    def get_current_tombola(self, current_date: datetime) -> TombolaEntity | None:
        """Get current tombola"""

    @abstractmethod
    def create(self, start_date: datetime, end_date: datetime) -> TombolaEntity:
        """Create tombola"""
