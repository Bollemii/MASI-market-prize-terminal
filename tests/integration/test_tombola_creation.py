import pytest
from datetime import datetime

from src.dataaccess.dao.tombola_dao import TombolaDAO
from src.models.tombola_model import TombolaModel
from src.dataaccess.entities.prize_entity import PrizeEntity
from src.dataaccess.repositories.tombola_repository import TombolaRepository
from src.dataaccess.repositories.prize_repository import PrizeRepository
from src.dataaccess.repositories.ticket_repository import TicketRepository
from src.dataaccess.repositories.user_repository import UserRepository
from src.dataaccess.repositories.city_repository import CityRepository
from src.utils.password_manager import PasswordManager
from src.utils.uuid_manager import UUIDManager


class TestTombolaCreationWithPrize:
    @pytest.fixture(scope="function", autouse=True, name="temp_folder")
    def create_temporary_testfolder(
        self, tmp_path_factory: pytest.TempPathFactory
    ) -> str:
        base_path = "test_create_tombola_with_prize"
        return str(tmp_path_factory.mktemp(base_path, True))

    @pytest.fixture(scope="function", autouse=True, name="prize_repository")
    def create_prize_repository(self, temp_folder: str) -> PrizeRepository:
        tombola_repository = TombolaRepository(temp_folder)
        return PrizeRepository(temp_folder, tombola_repository)

    @pytest.fixture(scope="function", autouse=True, name="tombola_dao")
    def create_tombola_dao(
        self, temp_folder: str, prize_repository: PrizeRepository
    ) -> TombolaDAO:
        password_manager = PasswordManager()
        uuid_manager = UUIDManager()
        tombola_repository = TombolaRepository(temp_folder)
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

    def test_tombola_created(
        self, tombola_dao: TombolaDAO, prize_repository: PrizeRepository
    ):
        tombola_model = TombolaModel(
            1, datetime.fromisoformat("2000-01-01 00:00:00"), datetime.now()
        )

        prize_list = []
        prize_list.append(PrizeEntity(None, None, "Un truc cool", 10, 0))
        prize_list.append(PrizeEntity(None, None, "Un truc moins cool", 5, 0))
        prize_list.append(PrizeEntity(None, None, "Un truc pas cool", 1, 0))
        tombola = tombola_dao.create_tombola_with_prize(
            tombola_model.start_date, tombola_model.end_date, prize_list, 100
        )
        assert tombola is not None
        assert tombola.id is not None

        prize_list = prize_repository.get_by_tombola_id(tombola.id)
        assert len(prize_list) == 3
