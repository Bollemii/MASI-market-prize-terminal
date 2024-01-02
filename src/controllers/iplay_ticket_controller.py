from abc import ABC, abstractmethod

from src.model.ticket_model import TicketModel
from src.model.user_model import UserModel


class IPlayTicketController(ABC):
    """Interface for PlayTicketController"""

    @abstractmethod
    def play_ticket(self, code: str, user: UserModel) -> TicketModel:
        """Play a ticket"""
