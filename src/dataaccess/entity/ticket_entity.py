from src.dataaccess.entity.user_entity import UserEntity
from src.dataaccess.entity.prize_entity import PrizeEntity


class TicketEntity:
    def __init__(self, code: str, prize: PrizeEntity | None, user: UserEntity | None):
        self.code = code
        self.prize = prize
        self.user = user
