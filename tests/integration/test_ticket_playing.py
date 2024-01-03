import pytest
from datetime import datetime

from src.controllers.play_ticket_controller import PlayTicketController
from src.dataaccess.dao.tombola_dao import TombolaDAO
from src.dataaccess.dao.ticket_dao import TicketDAO
from src.dataaccess.dao.prize_dao import PrizeDAO
from src.dataaccess.dao.user_dao import UserDAO
from src.dataaccess.dao.city_dao import CityDAO
from src.models.city_model import CityModel
from src.models.ticket_model import TicketModel
from src.models.prize_model import PrizeModel
from src.models.tombola_model import TombolaModel
from src.models.user_model import UserModel
from src.dataaccess.repositories.tombola_repository import TombolaRepository
from src.dataaccess.repositories.ticket_repository import TicketRepository
from src.dataaccess.repositories.prize_repository import PrizeRepository
from src.dataaccess.repositories.user_repository import UserRepository
from src.dataaccess.repositories.city_repository import CityRepository
from src.utils.password_manager import PasswordManager
from src.utils.uuid_manager import UUIDManager


class TestTicketPlaying:
    @pytest.fixture(scope="function", autouse=True, name="temp_folder")
    def create_temporary_testfolder(
        self, tmp_path_factory: pytest.TempPathFactory
    ) -> str:
        base_path = "test_ticket_playing"
        return str(tmp_path_factory.mktemp(base_path, True))

    @pytest.fixture(scope="function", autouse=True, name="user_dao")
    def create_user_dao(self, temp_folder: str) -> UserDAO:
        password_manager = PasswordManager()
        city_repository = CityRepository(temp_folder)
        user_repository = UserRepository(temp_folder, city_repository, password_manager)
        city_dao = CityDAO(city_repository)
        return UserDAO(user_repository, city_dao)

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

    @pytest.fixture(scope="function", autouse=True, name="prize_dao")
    def create_prize_dao(self, temp_folder: str, tombola_dao: TombolaDAO) -> PrizeDAO:
        tombola_repository = TombolaRepository(temp_folder)
        prize_repository = PrizeRepository(temp_folder, tombola_repository)
        return PrizeDAO(prize_repository, tombola_dao)

    @pytest.fixture(scope="function", autouse=True, name="ticket_dao")
    def create_ticket_dao(
        self,
        temp_folder: str,
        tombola_dao: TombolaDAO,
        user_dao: UserDAO,
        prize_dao: PrizeDAO,
    ) -> TicketDAO:
        tombola_repository = TombolaRepository(temp_folder)
        prize_repository = PrizeRepository(temp_folder, tombola_repository)
        user_repository = UserRepository(
            temp_folder, CityRepository(temp_folder), PasswordManager()
        )
        ticket_repository = TicketRepository(
            temp_folder,
            tombola_repository,
            user_repository,
            prize_repository,
        )
        return TicketDAO(ticket_repository, tombola_dao, user_dao, prize_dao)

    @pytest.fixture(scope="function", autouse=True, name="controller")
    def create_play_ticket_controller(
        self, ticket_dao: TicketDAO, prize_dao: PrizeDAO
    ) -> PlayTicketController:
        return PlayTicketController(ticket_dao, prize_dao)

    def test_ticket_user_assigned(
        self,
        user_dao: UserDAO,
        ticket_dao: TicketDAO,
        tombola_dao: TombolaDAO,
        controller: PlayTicketController,
    ):
        tombola = TombolaModel(
            1, datetime.fromisoformat("2000-01-01 00:00:00"), datetime.now()
        )
        tombola = tombola_dao.create(tombola.start_date, tombola.end_date)

        ticket = TicketModel("abc", tombola, None, None)
        ticket = ticket_dao.create(ticket.code, ticket.tombola.id, None)

        user = UserModel(1, "test@test.test", "password", CityModel(1, "test", "1111"))
        user = user_dao.register(
            user.email, user.password, user.city.name, user.city.postal_code
        )

        ticket_played = controller.play_ticket(ticket.code, user)

        assert ticket_played is not None
        assert ticket_played.user is not None
        assert ticket_played.user.id == user.id

    def test_ticket_tombola_won(
        self,
        user_dao: UserDAO,
        ticket_dao: TicketDAO,
        tombola_dao: TombolaDAO,
        prize_dao: PrizeDAO,
        controller: PlayTicketController,
    ):
        tombola = TombolaModel(
            1, datetime.fromisoformat("2000-01-01 00:00:00"), datetime.now()
        )
        tombola = tombola_dao.create(tombola.start_date, tombola.end_date)

        prize = PrizeModel(1, tombola, "test", 100, 0)
        assert prize.tombola is not None
        prize = prize_dao.create(
            prize.tombola.id, prize.description, prize.nb_available
        )

        ticket = TicketModel("abc", tombola, None, None)
        ticket = ticket_dao.create(ticket.code, ticket.tombola.id, prize.id)

        user = UserModel(1, "test@test.test", "password", CityModel(1, "test", "1111"))
        user = user_dao.register(
            user.email, user.password, user.city.name, user.city.postal_code
        )

        ticket_played = controller.play_ticket(ticket.code, user)

        assert ticket_played is not None
        assert ticket.prize is not None and ticket_played.prize is not None
        assert ticket_played.prize.id == ticket.prize.id
        assert ticket_played.prize.nb_won == ticket.prize.nb_won + 1
        assert ticket_played.prize.nb_available == ticket.prize.nb_available - 1
