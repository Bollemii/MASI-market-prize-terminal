from src.dataaccess.dao.user_dao import UserDAO
from src.dataaccess.dao.prize_dao import PrizeDAO
from src.dataaccess.repository.ticket_repository import TicketRepository
from src.dataaccess.entity.ticket_entity import TicketEntity
from src.model.ticket_model import TicketModel
from src.model.user_model import UserModel


class TicketDAO:
    def __init__(self, base_path: str):
        self.ticket_repository = TicketRepository(base_path)
        self.user_dao = UserDAO(base_path)
        self.prize_dao = PrizeDAO(base_path)

    def convert_ticket_entity_to_ticket_model(
        self, entity: TicketEntity
    ) -> TicketModel:
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
            prize,
            user,
        )

    def get_by_code(self, code: str) -> TicketModel:
        entity = self.ticket_repository.get_by_code(code)
        return self.convert_ticket_entity_to_ticket_model(entity)

    def assign_user(self, ticket: TicketModel, user: UserModel) -> TicketModel:
        entity = self.ticket_repository.assign_user(ticket.code, user.id)
        return self.convert_ticket_entity_to_ticket_model(entity)
