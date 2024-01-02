from src.dataaccess.dao.user_dao import UserDAO
from src.dataaccess.dao.prize_dao import PrizeDAO
from src.dataaccess.dao.tombola_dao import TombolaDAO
from src.dataaccess.repository.iticket_repository import ITicketRepository
from src.dataaccess.entity.ticket_entity import TicketEntity
from src.exception.ticket_not_found_exception import TicketNotFoundException
from src.model.ticket_model import TicketModel
from src.model.user_model import UserModel


class TicketDAO:
    def __init__(
        self,
        ticket_repository: ITicketRepository,
        tombola_dao: TombolaDAO,
        user_dao: UserDAO,
        prize_dao: PrizeDAO,
    ):
        self.ticket_repository = ticket_repository
        self.tombola_dao = tombola_dao
        self.user_dao = user_dao
        self.prize_dao = prize_dao

    def _convert_ticket_entity_to_ticket_model(
        self, entity: TicketEntity
    ) -> TicketModel:
        tombola = self.tombola_dao._convert_tombola_entity_to_tombola_model(
            entity.tombola
        )
        user = (
            self.user_dao._convert_user_entity_to_user_model(entity.user)
            if entity.user
            else None
        )
        prize = (
            self.prize_dao._convert_prize_entity_to_prize_model(entity.prize)
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
        return self._convert_ticket_entity_to_ticket_model(entity)

    def assign_user(self, ticket: TicketModel, user: UserModel) -> TicketModel:
        entity = self.ticket_repository.assign_user(ticket.code, user.id)
        return self._convert_ticket_entity_to_ticket_model(entity)

    def create(self, code: str, tombola_id: int, prize_id: int | None) -> TicketModel:
        entity = self.ticket_repository.create(code, tombola_id, prize_id)
        return self._convert_ticket_entity_to_ticket_model(entity)

    def get_by_tombola(self, tombola_id: int) -> list[TicketModel]:
        entities = self.ticket_repository.get_by_tombola(tombola_id)
        return [
            self._convert_ticket_entity_to_ticket_model(entity) for entity in entities
        ]
