from src.model.user_model import UserModel
from src.model.prize_model import PrizeModel


class TicketModel:
    def __init__(self, code: str, prize: PrizeModel | None, user: UserModel | None):
        self.code = code
        self.prize = prize
        self.user = user
