from src.model.tombola_model import TombolaModel
from src.model.user_model import UserModel
from src.model.prize_model import PrizeModel


class TicketModel:
    """Ticket model"""

    def __init__(
        self,
        code: str,
        tombola: TombolaModel,
        prize: PrizeModel | None,
        user: UserModel | None,
    ):
        self.code = code
        self.tombola = tombola
        self.prize = prize
        self.user = user
