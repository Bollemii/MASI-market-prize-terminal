from src.dataaccess.dao.ticket_dao import TicketDAO
from src.dataaccess.dao.prize_dao import PrizeDAO
from src.exception.ticket_not_found_exception import TicketNotFoundException
from src.model.ticket_model import TicketModel
from src.model.user_model import UserModel


class PlayTicketController:
    def __init__(self, ticket_dao: TicketDAO, prize_dao: PrizeDAO):
        self.ticket_dao = ticket_dao
        self.prize_dao = prize_dao

    def play_ticket(self, code: str, user: UserModel) -> TicketModel:
        ticket = self.ticket_dao.get_by_code(code)
        if not ticket:
            raise TicketNotFoundException()
        if ticket.user:
            raise Exception("Ticket already played")
        ticket = self.ticket_dao.assign_user(ticket, user)
        if ticket.prize:
            ticket.prize = self.prize_dao.prize_won(ticket.prize)
        return ticket
