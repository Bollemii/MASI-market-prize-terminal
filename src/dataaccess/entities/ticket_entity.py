from src.dataaccess.entities.tombola_entity import TombolaEntity
from src.dataaccess.entities.user_entity import UserEntity
from src.dataaccess.entities.prize_entity import PrizeEntity


class TicketEntity:
    """Ticket entity"""

    def __init__(
        self,
        code: str,
        tombola: TombolaEntity,
        prize: PrizeEntity | None,
        user: UserEntity | None,
    ):
        self.code = code
        self.tombola = tombola
        self.prize = prize
        self.user = user
