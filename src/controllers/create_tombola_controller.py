from datetime import datetime

from src.controllers.icreate_tombola_controller import ICreateTombolaController
from src.dataaccess.dao.itombola_dao import ITombolaDAO
from src.model.prize_model import PrizeModel
from src.model.tombola_model import TombolaModel


class CreateTombolaController(ICreateTombolaController):
    """Create tombola controller"""

    def __init__(self, tombola_dao: ITombolaDAO):
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
