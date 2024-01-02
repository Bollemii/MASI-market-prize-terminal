import pytest
from datetime import datetime

from src.dataaccess.dao.tombola_dao import TombolaDAO
from src.dataaccess.entity.tombola_entity import TombolaEntity
from src.dataaccess.repository.tombola_repository import TombolaRepository
from src.dataaccess.repository.prize_repository import PrizeRepository
from src.dataaccess.repository.ticket_repository import TicketRepository
from src.dataaccess.repository.user_repository import UserRepository
from src.dataaccess.repository.city_repository import CityRepository
from src.utils.password_manager import PasswordManager
from src.utils.uuid_manager import UUIDManager


class TestTombolaDAO:
    @pytest.fixture(scope="function", autouse=True, name="temp_folder")
    def create_temporary_testfolder(
        self, tmp_path_factory: pytest.TempPathFactory
    ) -> str:
        base_path = "test_tombola_dao"
        return str(tmp_path_factory.mktemp(base_path, True))

    @pytest.fixture(scope="function", autouse=True, name="tombola_dao")
    def create_tombola_dao(self, temp_folder: str) -> TombolaDAO:
        password_manager = PasswordManager()
        uuid_manager = UUIDManager()
        tombola_repository = TombolaRepository(temp_folder)
        prize_repository = PrizeRepository(temp_folder, tombola_repository)
        city_repository = CityRepository(temp_folder)
        user_repository = UserRepository(temp_folder, city_repository, password_manager)
        ticket_repository = TicketRepository(
            temp_folder,
            tombola_repository,
            user_repository,
            prize_repository,
        )
        return TombolaDAO(
            tombola_repository,
            prize_repository,
            ticket_repository,
            uuid_manager,
        )

    def test_converter_entity_to_model(self, tombola_dao: TombolaDAO):
        entity = TombolaEntity(
            1,
            datetime.fromisoformat("2000-01-01 00:00:00"),
            datetime.fromisoformat("9999-01-01 00:00:00"),
        )

        model = tombola_dao.convert_tombola_entity_to_tombola_model(entity)

        assert model.id == entity.id
        assert model.start_date == entity.start_date
        assert model.end_date == entity.end_date
