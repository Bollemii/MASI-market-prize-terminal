from src.dataaccess.repository.prize_repository import PrizeRepository
from src.dataaccess.entity.prize_entity import PrizeEntity
from src.model.prize_model import PrizeModel


class PrizeDAO:
    def __init__(self, base_path: str):
        self.prize_repository = PrizeRepository(base_path)

    def convert_prize_entity_to_prize_model(self, entity: PrizeEntity) -> PrizeModel:
        return PrizeModel(
            entity.id,
            entity.description,
            entity.nb_available,
            entity.nb_won,
        )
