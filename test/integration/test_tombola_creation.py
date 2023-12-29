import pytest
from datetime import datetime

from src.dataaccess.dao.tombola_dao import TombolaDAO
from src.dataaccess.entity.prize_entity import PrizeEntity
from src.model.tombola_model import TombolaModel
from src.dataaccess.repository.prize_repository import PrizeRepository


class TestTombolaCreationWithPrize:
    @pytest.fixture(scope="function", autouse=True, name="temp_folder")
    def create_temporary_testfolder(
        self, tmp_path_factory: pytest.TempPathFactory
    ) -> str:
        base_path = "test_create_tombola_with_prize"
        return str(tmp_path_factory.mktemp(base_path, True))

    def test_tombola_created(self, temp_folder):
        tombola_dao = TombolaDAO(temp_folder)
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
        prize_repository = PrizeRepository(temp_folder)
        prize_list = prize_repository.get_by_tombola_id(tombola.id)
        assert len(prize_list) == 3
