from src.dataaccess.entity.tombola_entity import TombolaEntity
from src.dataaccess.repository.tombola_repository import TombolaRepository
from src.model.tombola_model import TombolaModel


class TombolaDAO:
    def __init__(self, base_path: str):
        self.tombola_repository = TombolaRepository(base_path)

    def convert_tombola_entity_to_tombola_model(
        self, entity: TombolaEntity
    ) -> TombolaModel:
        return TombolaModel(entity.id, entity.start_date, entity.end_date)
