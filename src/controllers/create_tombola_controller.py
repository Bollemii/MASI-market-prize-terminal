from datetime import datetime

from src.dataaccess.dao.tombola_dao import TombolaDAO
from src.model.prize_model import PrizeModel
from src.model.tombola_model import TombolaModel


class CreateTombolaController:
    def __init__(self, tombola_dao: TombolaDAO):
        self.tombola_dao = tombola_dao

    def create_tombola(
        self,
        start_date: datetime,
        end_date: datetime,
        prizes: list[PrizeModel],
        nb_tickets: int,
    ) -> TombolaModel:
        return self.tombola_dao.create_tombola_with_prize(
            start_date, end_date, prizes, nb_tickets
        )
