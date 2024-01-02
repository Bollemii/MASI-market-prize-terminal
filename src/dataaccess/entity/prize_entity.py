from src.dataaccess.entity.tombola_entity import TombolaEntity


class PrizeEntity:
    def __init__(
        self,
        id: int | None,
        tombola: TombolaEntity | None,
        description: str,
        nb_available: int,
        nb_won: int,
    ):
        self.id = id
        self.tombola = tombola
        self.description = description
        self.nb_available = nb_available
        self.nb_won = nb_won
