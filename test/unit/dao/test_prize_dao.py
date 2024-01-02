from datetime import datetime
import pytest

from src.dataaccess.dao.prize_dao import PrizeDAO
from src.dataaccess.dao.tombola_dao import TombolaDAO
from src.dataaccess.entity.prize_entity import PrizeEntity
from src.dataaccess.entity.tombola_entity import TombolaEntity
from src.dataaccess.repository.city_repository import CityRepository
from src.dataaccess.repository.prize_repository import PrizeRepository
from src.dataaccess.repository.ticket_repository import TicketRepository
from src.dataaccess.repository.tombola_repository import TombolaRepository
from src.dataaccess.repository.user_repository import UserRepository
from src.utils.password_manager import PasswordManager
from src.utils.uuid_manager import UUIDManager


class TestPrizeDAO:
    @pytest.fixture(scope="function", autouse=True, name="temp_folder")
    def create_temporary_testfolder(
        self, tmp_path_factory: pytest.TempPathFactory
    ) -> str:
        base_path = "test_prize_dao"
        return str(tmp_path_factory.mktemp(base_path, True))

    @pytest.fixture(scope="function", autouse=True, name="prize_dao")
    def create_prize_dao(self, temp_folder: str) -> PrizeDAO:
        password_manager = PasswordManager()
        uuid_manager = UUIDManager()
        tombola_repository = TombolaRepository(temp_folder)
        city_repository = CityRepository(temp_folder)
        user_repository = UserRepository(temp_folder, city_repository, password_manager)
        prize_repository = PrizeRepository(temp_folder, tombola_repository)
        ticket_repository = TicketRepository(
            temp_folder,
            tombola_repository,
            user_repository,
            prize_repository,
        )
        tombola_dao = TombolaDAO(
            tombola_repository,
            prize_repository,
            ticket_repository,
            uuid_manager,
        )
        return PrizeDAO(prize_repository, tombola_dao)

    def test_converter_entity_to_model(self, prize_dao: PrizeDAO):
        tombola = TombolaEntity(
            1, datetime.fromisoformat("2000-01-01 00:00:00"), datetime.now()
        )
        entity = PrizeEntity(1, tombola, "Un truc cool", 10, 5)

        model = prize_dao.convert_prize_entity_to_prize_model(entity)

        assert model.id == entity.id
        assert model.tombola is not None
        assert entity.tombola is not None
        assert model.tombola.id == entity.tombola.id
        assert model.description == entity.description
        assert model.nb_available == entity.nb_available
        assert model.nb_won == entity.nb_won
