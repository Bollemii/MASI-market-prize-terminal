from src.models.tombola_model import TombolaModel


class PrizeModel:
    """Prize model"""

    def __init__(
        self,
        id: int | None,
        tombola: TombolaModel | None,
        description: str,
        nb_available: int,
        nb_won: int = 0,
    ):
        self.id = id
        self.tombola = tombola
        self.description = description
        self.nb_available = nb_available
        self.nb_won = nb_won
