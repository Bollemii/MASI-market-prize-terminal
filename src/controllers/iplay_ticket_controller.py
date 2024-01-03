from abc import ABC, abstractmethod

from src.models.ticket_model import TicketModel
from src.models.user_model import UserModel


class IPlayTicketController(ABC):
    """Interface for PlayTicketController"""

    @abstractmethod
    def play_ticket(self, code: str, user: UserModel) -> TicketModel:
        """Play a ticket"""
