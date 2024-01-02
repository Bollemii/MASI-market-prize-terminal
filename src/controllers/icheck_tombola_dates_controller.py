from abc import ABC, abstractmethod
from datetime import datetime


class ICheckTombolaDatesController(ABC):
    """Interface for CheckTombolaDatesController"""

    @abstractmethod
    def is_period_available(self, start_date: datetime, end_date: datetime) -> bool:
        """Check if there are tombola in dates range"""
