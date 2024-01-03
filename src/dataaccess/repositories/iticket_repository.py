from abc import ABC, abstractmethod

from src.dataaccess.entities.ticket_entity import TicketEntity


class ITicketRepository(ABC):
    """Interface for TicketRepository"""

    @abstractmethod
    def get_by_code(self, code: str) -> TicketEntity | None:
        """Get ticket by code"""

    @abstractmethod
    def assign_user(self, code: str, user_id: int) -> TicketEntity:
        """Assign user"""

    @abstractmethod
    def assign_prize(self, code: str, prize_id: int) -> TicketEntity:
        """Assign prize"""

    @abstractmethod
    def create(self, code: str, tombola_id: int, prize_id: int | None) -> TicketEntity:
        """Create ticket"""

    @abstractmethod
    def get_by_tombola(self, tombola_id: int) -> list[TicketEntity]:
        """Get ticket by tombola id"""
