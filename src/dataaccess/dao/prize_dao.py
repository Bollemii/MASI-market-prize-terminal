from src.dataaccess.dao.tombola_dao import TombolaDAO
from src.dataaccess.repository.iprize_repository import IPrizeRepository
from src.dataaccess.entity.prize_entity import PrizeEntity
from src.exception.prize_not_found_exception import PrizeNotFoundException
from src.model.prize_model import PrizeModel


class PrizeDAO:
    def __init__(self, prize_repository: IPrizeRepository, tombola_dao: TombolaDAO):
        self.prize_repository = prize_repository
        self.tombola_dao = tombola_dao

    def _convert_prize_entity_to_prize_model(self, entity: PrizeEntity) -> PrizeModel:
        return PrizeModel(
            entity.id,
            self.tombola_dao._convert_tombola_entity_to_tombola_model(entity.tombola),
            entity.description,
            entity.nb_available,
            entity.nb_won,
        )

    def prize_won(self, prize: PrizeModel) -> PrizeModel:
        if prize.id is None:
            raise PrizeNotFoundException()
        entity = self.prize_repository.prize_won(prize.id)
        return self._convert_prize_entity_to_prize_model(entity)

    def create(self, tombola_id: int, description: str, quantity: int) -> PrizeModel:
        entity = self.prize_repository.create(tombola_id, description, quantity)
        return self._convert_prize_entity_to_prize_model(entity)
