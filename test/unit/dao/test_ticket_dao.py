import pytest
from datetime import datetime

from src.dataaccess.dao.ticket_dao import TicketDAO
from src.dataaccess.dao.tombola_dao import TombolaDAO
from src.dataaccess.dao.user_dao import UserDAO
from src.dataaccess.dao.prize_dao import PrizeDAO
from src.dataaccess.dao.city_dao import CityDAO
from src.dataaccess.entity.city_entity import CityEntity
from src.dataaccess.entity.prize_entity import PrizeEntity
from src.dataaccess.entity.ticket_entity import TicketEntity
from src.dataaccess.entity.tombola_entity import TombolaEntity
from src.dataaccess.entity.user_entity import UserEntity
from src.dataaccess.repository.city_repository import CityRepository
from src.dataaccess.repository.prize_repository import PrizeRepository
from src.dataaccess.repository.ticket_repository import TicketRepository
from src.dataaccess.repository.tombola_repository import TombolaRepository
from src.dataaccess.repository.user_repository import UserRepository
from src.utils.password_manager import PasswordManager
from src.utils.uuid_manager import UUIDManager


class TestTicketDAO:
    @pytest.fixture(scope="function", autouse=True, name="temp_folder")
    def create_temporary_testfolder(
        self, tmp_path_factory: pytest.TempPathFactory
    ) -> str:
        base_path = "test_ticket_dao"
        return str(tmp_path_factory.mktemp(base_path, True))

    @pytest.fixture(scope="function", autouse=True, name="ticket_dao")
    def create_ticket_dao(self, temp_folder: str) -> TicketDAO:
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
        tombola_dao = TombolaDAO(
            tombola_repository,
            prize_repository,
            ticket_repository,
            uuid_manager,
        )
        prize_dao = PrizeDAO(prize_repository, tombola_dao)
        city_dao = CityDAO(city_repository)
        user_dao = UserDAO(user_repository, city_dao)
        return TicketDAO(ticket_repository, tombola_dao, user_dao, prize_dao)

    def test_converter_entity_to_model(self, ticket_dao: TicketDAO):
        city = CityEntity(1, "name", "postal_code")
        user = UserEntity(1, "email", "password", city)
        tombola = TombolaEntity(
            1,
            datetime.fromisoformat("2000-01-01 00:00:00"),
            datetime.fromisoformat("9999-01-01 00:00:00"),
        )
        prize = PrizeEntity(1, tombola, "description", 100, 0)
        entity = TicketEntity("abc", tombola, prize, user)

        model = ticket_dao.convert_ticket_entity_to_ticket_model(entity)

        assert model.code == entity.code
        assert model.tombola.id == entity.tombola.id
        assert entity.prize is not None and model.prize is not None
        assert model.prize.id == entity.prize.id
        assert entity.user is not None and model.user is not None
        assert model.user.id == entity.user.id
