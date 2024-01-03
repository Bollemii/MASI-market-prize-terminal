from src.dataaccess.dao.iticket_dao import ITicketDAO
from src.dataaccess.dao.iuser_dao import IUserDAO
from src.dataaccess.dao.iprize_dao import IPrizeDAO
from src.dataaccess.dao.itombola_dao import ITombolaDAO
from src.dataaccess.repositories.iticket_repository import ITicketRepository
from src.dataaccess.entities.ticket_entity import TicketEntity
from src.exceptions.ticket_not_found_exception import TicketNotFoundException
from src.models.ticket_model import TicketModel
from src.models.user_model import UserModel


class TicketDAO(ITicketDAO):
    """Dao for Ticket"""

    def __init__(
        self,
        ticket_repository: ITicketRepository,
        tombola_dao: ITombolaDAO,
        user_dao: IUserDAO,
        prize_dao: IPrizeDAO,
    ):
        self.ticket_repository = ticket_repository
        self.tombola_dao = tombola_dao
        self.user_dao = user_dao
        self.prize_dao = prize_dao

    def convert_ticket_entity_to_ticket_model(
        self, entity: TicketEntity
    ) -> TicketModel:
        tombola = self.tombola_dao.convert_tombola_entity_to_tombola_model(
            entity.tombola
        )
        user = (
            self.user_dao.convert_user_entity_to_user_model(entity.user)
            if entity.user
            else None
        )
        prize = (
            self.prize_dao.convert_prize_entity_to_prize_model(entity.prize)
            if entity.prize
            else None
        )
        return TicketModel(
            entity.code,
            tombola,
            prize,
            user,
        )

    def get_by_code(self, code: str) -> TicketModel:
        entity = self.ticket_repository.get_by_code(code)
        if not entity:
            raise TicketNotFoundException()
        return self.convert_ticket_entity_to_ticket_model(entity)

    def assign_user(self, ticket: TicketModel, user: UserModel) -> TicketModel:
        entity = self.ticket_repository.assign_user(ticket.code, user.id)
        return self.convert_ticket_entity_to_ticket_model(entity)

    def create(self, code: str, tombola_id: int, prize_id: int | None) -> TicketModel:
        entity = self.ticket_repository.create(code, tombola_id, prize_id)
        return self.convert_ticket_entity_to_ticket_model(entity)

    def get_by_tombola(self, tombola_id: int) -> list[TicketModel]:
        entities = self.ticket_repository.get_by_tombola(tombola_id)
        return [
            self.convert_ticket_entity_to_ticket_model(entity) for entity in entities
        ]
