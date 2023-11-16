from datetime import datetime

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

    def get_current_tombola(self) -> TombolaModel | None:
        result = self.tombola_repository.get_current_tombola(datetime.now())
        if not result:
            return None
        return self.convert_tombola_entity_to_tombola_model(result)

    def create(self, start_date: datetime, end_date: datetime) -> TombolaModel:
        entity = self.tombola_repository.create(start_date, end_date)
        return self.convert_tombola_entity_to_tombola_model(entity)
