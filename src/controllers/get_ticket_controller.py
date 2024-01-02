from src.dataaccess.dao.ticket_dao import TicketDAO
from src.model.ticket_model import TicketModel


class GetTicketController:
    def __init__(self, ticket_dao: TicketDAO):
        self.ticket_dao = ticket_dao

    def get_ticket_by_tombola(self, tombola_id: int) -> list[TicketModel]:
        return self.ticket_dao.get_by_tombola(tombola_id)
