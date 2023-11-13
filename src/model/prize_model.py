from src.model.tombola_model import TombolaModel


class PrizeModel:
    def __init__(
        self,
        id: int,
        tombola: TombolaModel,
        description: str,
        nb_available: int,
        nb_won: int,
    ):
        self.id = id
        self.tombola = tombola
        self.description = description
        self.nb_available = nb_available
        self.nb_won = nb_won
