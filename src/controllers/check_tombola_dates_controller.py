from datetime import datetime

from src.controllers.icheck_tombola_dates_controller import ICheckTombolaDatesController
from src.dataaccess.dao.itombola_dao import ITombolaDAO


class CheckTombolaDatesController(ICheckTombolaDatesController):
    """Check tombola dates controller"""

    def __init__(self, tombola_dao: ITombolaDAO):
        self.tombola_dao = tombola_dao

    def is_period_available(self, start_date: datetime, end_date: datetime) -> bool:
        """Check if there are tombola in dates range"""
        return not self.tombola_dao.are_tombolas_in_dates_range(start_date, end_date)
