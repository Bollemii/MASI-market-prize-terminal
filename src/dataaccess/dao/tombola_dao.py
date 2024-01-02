from datetime import datetime

from src.dataaccess.entity.tombola_entity import TombolaEntity
from src.dataaccess.repository.tombola_repository import TombolaRepository
from src.dataaccess.repository.ticket_repository import TicketRepository
from src.dataaccess.repository.prize_repository import PrizeRepository
from src.model.tombola_model import TombolaModel
from src.model.prize_model import PrizeModel
from src.utils.uuid_manager import UUIDManager


class TombolaDAO:
    def __init__(
        self,
        tombola_repository: TombolaRepository,
        prize_repository: PrizeRepository,
        ticket_repository: TicketRepository,
        uuid_manager: UUIDManager,
    ):
        self.tombola_repository = tombola_repository
        self.prize_repository = prize_repository
        self.ticket_repository = ticket_repository
        self.uuid_manager = uuid_manager

    def _convert_tombola_entity_to_tombola_model(
        self, entity: TombolaEntity
    ) -> TombolaModel:
        return TombolaModel(entity.id, entity.start_date, entity.end_date)

    def get_current_tombola(self) -> TombolaModel | None:
        result = self.tombola_repository.get_current_tombola(datetime.now())
        if not result:
            return None
        return self._convert_tombola_entity_to_tombola_model(result)

    def create(self, start_date: datetime, end_date: datetime) -> TombolaModel:
        entity = self.tombola_repository.create(start_date, end_date)
        return self._convert_tombola_entity_to_tombola_model(entity)

    def create_tombola_with_prize(
        self,
        start_date: datetime,
        end_date: datetime,
        prizes: list[PrizeModel],
        nb_tickets: int,
    ) -> TombolaModel:
        tombola_entity = self.tombola_repository.create(start_date, end_date)

        total_prizes = 0
        for prize in prizes:
            if prize.id is None:
                prize = self.prize_repository.create(
                    tombola_entity.id, prize.description, prize.nb_available
                )
            total_prizes += prize.nb_available
            for i in range(prize.nb_available):
                self.ticket_repository.create(
                    self.uuid_manager.generate(), tombola_entity.id, prize.id
                )

        for i in range(nb_tickets - total_prizes):
            self.ticket_repository.create(
                self.uuid_manager.generate(), tombola_entity.id, None
            )

        tombola_entity = self.tombola_repository.get_by_id(tombola_entity.id)
        if tombola_entity is None:
            raise Exception("The tombola was not created")
        return self._convert_tombola_entity_to_tombola_model(tombola_entity)
