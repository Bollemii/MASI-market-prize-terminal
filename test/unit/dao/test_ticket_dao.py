import pytest
from datetime import datetime

from src.dataaccess.dao.ticket_dao import TicketDAO
from src.dataaccess.entity.city_entity import CityEntity
from src.dataaccess.entity.prize_entity import PrizeEntity
from src.dataaccess.entity.ticket_entity import TicketEntity
from src.dataaccess.entity.tombola_entity import TombolaEntity
from src.dataaccess.entity.user_entity import UserEntity


class TestTicketDAO:
    @pytest.fixture(scope="function", autouse=True, name="temp_folder")
    def create_temporary_testfolder(
        self, tmp_path_factory: pytest.TempPathFactory
    ) -> str:
        base_path = "test_city_repository"
        return str(tmp_path_factory.mktemp(base_path, True))

    def test_converter_entity_to_model(self, temp_folder):
        ticket_dao = TicketDAO(temp_folder)

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
