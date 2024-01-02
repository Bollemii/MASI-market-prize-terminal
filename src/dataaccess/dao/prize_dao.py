from src.dataaccess.dao.tombola_dao import TombolaDAO
from src.dataaccess.repository.prize_repository import PrizeRepository
from src.dataaccess.entity.prize_entity import PrizeEntity
from src.exception.prize_not_found_exception import PrizeNotFoundException
from src.model.prize_model import PrizeModel


class PrizeDAO:
    def __init__(self, base_path: str):
        self.prize_repository = PrizeRepository(base_path)
        self.tombola_dao = TombolaDAO(base_path)

    def convert_prize_entity_to_prize_model(self, entity: PrizeEntity) -> PrizeModel:
        return PrizeModel(
            entity.id,
            self.tombola_dao.convert_tombola_entity_to_tombola_model(entity.tombola),
            entity.description,
            entity.nb_available,
            entity.nb_won,
        )

    def prize_won(self, prize: PrizeModel) -> PrizeModel:
        if prize.id is None:
            raise PrizeNotFoundException()
        entity = self.prize_repository.prize_won(prize.id)
        return self.convert_prize_entity_to_prize_model(entity)

    def create(self, tombola_id: int, description: str, quantity: int) -> PrizeModel:
        entity = self.prize_repository.create(tombola_id, description, quantity)
        return self.convert_prize_entity_to_prize_model(entity)
