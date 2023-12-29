from src.dataaccess.dao.tombola_dao import TombolaDAO
from src.dataaccess.entity.prize_entity import PrizeEntity
from datetime import datetime


class CreateTombolaController:
    def __init__(self, base_path: str):
        self.tombola_dao = TombolaDAO(base_path)

    def create_tombola(
        self, start_date: datetime, end_date: datetime, prizes: [PrizeEntity]
    ):
        self.tombola_dao.create_tombola_with_prize(start_date, end_date, prizes)
