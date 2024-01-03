from src.controllers.iget_current_tombola_controller import IGetCurrentTombolaController
from src.dataaccess.dao.itombola_dao import ITombolaDAO
from src.models.tombola_model import TombolaModel


class GetCurrentTombolaController(IGetCurrentTombolaController):
    """Get current tombola controller"""

    def __init__(self, tombola_dao: ITombolaDAO):
        self.tombola_dao = tombola_dao

    def get_current_tombola(self) -> TombolaModel | None:
        return self.tombola_dao.get_current_tombola()
