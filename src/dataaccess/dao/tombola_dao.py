from datetime import datetime

from src.dataaccess.entity.prize_entity import PrizeEntity
from src.dataaccess.entity.tombola_entity import TombolaEntity
from src.dataaccess.repository.tombola_repository import TombolaRepository
from src.dataaccess.repository.ticket_repository import TicketRepository
from src.dataaccess.repository.prize_repository import PrizeRepository
from src.model.tombola_model import TombolaModel
from src.dataaccess.repository.common.sqlite_repository import SqliteRepository
from src.utils.uuid_manager import UUIDManager


class TombolaDAO:
    def __init__(self, base_path: str):
        self.tombola_repository = TombolaRepository(base_path)
        self.sqlite_repository = SqliteRepository(base_path)
        self.prize_repository = PrizeRepository(base_path)
        self.ticket_repository = TicketRepository(base_path)
        self.uuid_manager = UUIDManager()

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

    def create_tombola_with_prize(
        self,
        start_date: datetime,
        end_date: datetime,
        prizes: [PrizeEntity],
        nb_lose: int,
    ) -> TombolaModel:
        try:
            entity = self.tombola_repository.create(start_date, end_date)
            for prize in prizes:
                if prize.id is None:
                    prize = self.prize_repository.create(
                        entity.id, prize.description, prize.nb_available
                    )
                for i in range(prize.nb_available):
                    self.ticket_repository.create(
                        self.uuid_manager.generate(), entity.id, prize.id
                    )
            for i in range(nb_lose):
                self.ticket_repository.create(
                    self.uuid_manager.generate(), entity.id, None
                )
        except Exception as e:
            raise e
        return self.convert_tombola_entity_to_tombola_model(entity)
