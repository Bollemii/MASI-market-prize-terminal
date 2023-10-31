from dataaccess.dao import ticket_dao
from models.user import User
from models.prize import Prize


class Ticket:
    def __init__(self, code: str, prize: Prize | None, user: User | None):
        self.code = code
        self.prize = prize
        self.user = user

    @staticmethod
    def play(code: str, user: User) -> "Ticket":
        ticket = ticket_dao.get_by_code(code)
        if ticket.user is not None:
            raise Exception("Ticket is already used")
        return ticket_dao.assign_user(ticket, user)
