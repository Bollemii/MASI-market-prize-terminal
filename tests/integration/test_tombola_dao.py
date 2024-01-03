import pytest
from datetime import datetime

from src.dataaccess.dao.tombola_dao import TombolaDAO
from src.models.tombola_model import TombolaModel
from src.dataaccess.repositories.tombola_repository import TombolaRepository
from src.dataaccess.repositories.prize_repository import PrizeRepository
from src.dataaccess.repositories.ticket_repository import TicketRepository
from src.dataaccess.repositories.user_repository import UserRepository
from src.dataaccess.repositories.city_repository import CityRepository
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

    def test_tombola_created(self, tombola_dao: TombolaDAO):
        tombola = TombolaModel(
            1, datetime.fromisoformat("2000-01-01 00:00:00"), datetime.now()
        )
        tombola = tombola_dao.create(tombola.start_date, tombola.end_date)

        assert tombola is not None
        assert tombola.start_date == tombola.start_date
        assert tombola.end_date == tombola.end_date

    def test_get_current_tombola(self, tombola_dao: TombolaDAO):
        tombola = TombolaModel(
            1,
            datetime.fromisoformat("2000-01-01 00:00:00"),
            datetime.fromisoformat("9999-01-01 00:00:00"),
        )
        tombola = tombola_dao.create(tombola.start_date, tombola.end_date)

        current_tombola = tombola_dao.get_current_tombola()

        assert current_tombola is not None
        assert current_tombola.id == tombola.id
        assert current_tombola.start_date == tombola.start_date
        assert current_tombola.end_date == tombola.end_date

    def test_are_tombolas_in_range(self, tombola_dao: TombolaDAO):
        tombola = TombolaModel(
            1,
            datetime.fromisoformat("2000-01-01 00:00:00"),
            datetime.fromisoformat("9999-01-01 00:00:00"),
        )
        tombola = tombola_dao.create(tombola.start_date, tombola.end_date)

        are_tombolas_in_range = tombola_dao.are_tombolas_in_dates_range(
            datetime.fromisoformat("2024-01-01 00:00:00"),
            datetime.fromisoformat("2025-01-01 00:00:00"),
        )

        assert are_tombolas_in_range

    def test_are_not_tombolas_in_range(self, tombola_dao: TombolaDAO):
        tombola = TombolaModel(
            1,
            datetime.fromisoformat("3000-01-01 00:00:00"),
            datetime.fromisoformat("9999-01-01 00:00:00"),
        )
        tombola = tombola_dao.create(tombola.start_date, tombola.end_date)

        are_tombolas_in_range = tombola_dao.are_tombolas_in_dates_range(
            datetime.fromisoformat("2024-01-01 00:00:00"),
            datetime.fromisoformat("2025-01-01 00:00:00"),
        )

        assert not are_tombolas_in_range

    def test_are_tombolas_in_range_border(self, tombola_dao: TombolaDAO):
        tombola = TombolaModel(
            1,
            datetime.fromisoformat("3000-01-01 00:00:00"),
            datetime.fromisoformat("9999-01-01 00:00:00"),
        )
        tombola = tombola_dao.create(tombola.start_date, tombola.end_date)

        are_tombolas_in_range = tombola_dao.are_tombolas_in_dates_range(
            datetime.fromisoformat("2024-01-01 00:00:00"),
            datetime.fromisoformat("3000-01-01 00:00:00"),
        )

        assert are_tombolas_in_range
