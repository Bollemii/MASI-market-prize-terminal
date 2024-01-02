from abc import ABC, abstractmethod

from src.dataaccess.entity.ticket_entity import TicketEntity
from src.model.ticket_model import TicketModel
from src.model.user_model import UserModel


class ITicketDAO(ABC):
    """Interface for TicketDao"""

    @abstractmethod
    def convert_ticket_entity_to_ticket_model(
        self, entity: TicketEntity
    ) -> TicketModel:
        """Convert ticket entity to ticket model"""

    @abstractmethod
    def get_by_code(self, code: str) -> TicketModel:
        """Get ticket by code"""

    @abstractmethod
    def assign_user(self, ticket: TicketModel, user: UserModel) -> TicketModel:
        """Assign user to ticket"""

    @abstractmethod
    def create(self, code: str, tombola_id: int, prize_id: int | None) -> TicketModel:
        """Create ticket"""

    @abstractmethod
    def get_by_tombola(self, tombola_id: int) -> list[TicketModel]:
        """Get tickets by tombola"""
