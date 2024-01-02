from abc import ABC, abstractmethod

from src.model.ticket_model import TicketModel


class IGetTicketController(ABC):
    """Interface for GetTicketController"""

    @abstractmethod
    def get_ticket_by_tombola(self, tombola_id: int) -> list[TicketModel]:
        """Get a ticket by tombola"""
