from prisma import Prisma  # type: ignore

from dataaccess.entity.user_entity import User
from dataaccess.entity.prize_entity import Prize


class Ticket:
    code: str
    prize: Prize | None
    user: User | None

    def __init__(self, code: str, prize: Prize | None, user: User | None):
        self.code = code
        self.prize = prize
        self.user = user

    @staticmethod
    def get_by_code(code: str) -> "Ticket":
        with Prisma() as db:
            ticket = db.ticket.find_first(
                where={"code": code},
            )
            if ticket is None:
                raise Exception("Ticket not found")
            return ticket

    @staticmethod
    def assign_user(code: str, user_id: int) -> "Ticket":
        with Prisma() as db:
            ticket = db.ticket.update(
                where={"code": code},
                data={"user_id": user_id},
            )
            return ticket
