import pytest
from datetime import datetime

from src.dataaccess.dao.tombola_dao import TombolaDAO
from src.dataaccess.dao.ticket_dao import TicketDAO
from src.dataaccess.dao.user_dao import UserDAO
from src.dataaccess.dao.prize_dao import PrizeDAO
from src.model.ticket_model import TicketModel
from src.model.tombola_model import TombolaModel
from src.model.prize_model import PrizeModel
from src.model.user_model import UserModel
from src.model.city_model import CityModel


class TestTicketDAO:
    @pytest.fixture(scope="function", autouse=True, name="temp_folder")
    def create_temporary_testfolder(
        self, tmp_path_factory: pytest.TempPathFactory
    ) -> str:
        base_path = "test_ticket_dao"
        return str(tmp_path_factory.mktemp(base_path, True))

    def test_ticket_created_without_user_prize(self, temp_folder):
        tombola_dao = TombolaDAO(temp_folder)
        tombola = TombolaModel(
            1, datetime.fromisoformat("2000-01-01 00:00:00"), datetime.now()
        )
        tombola = tombola_dao.create(tombola.start_date, tombola.end_date)

        ticket_dao = TicketDAO(temp_folder)
        ticket = TicketModel("abc", tombola, None, None)
        ticket = ticket_dao.create(ticket.code, ticket.tombola.id, None)

        assert ticket is not None
        assert ticket.code == ticket.code
        assert ticket.tombola.id == ticket.tombola.id
        assert ticket.prize is None
        assert ticket.user is None

    def test_ticket_created_with_prize(self, temp_folder):
        tombola_dao = TombolaDAO(temp_folder)
        tombola = TombolaModel(
            1, datetime.fromisoformat("2000-01-01 00:00:00"), datetime.now()
        )
        tombola = tombola_dao.create(tombola.start_date, tombola.end_date)

        prize_dao = PrizeDAO(temp_folder)
        prize = PrizeModel(1, tombola, "test", 100, 0)
        prize = prize_dao.create(
            prize.tombola.id, prize.description, prize.nb_available
        )

        ticket_dao = TicketDAO(temp_folder)
        ticket = TicketModel("abc", tombola, prize, None)
        ticket = ticket_dao.create(
            ticket.code, ticket.tombola.id, ticket.prize.id if ticket.prize else None
        )

        assert ticket is not None
        assert ticket.prize is not None
        assert ticket.prize.id == prize.id

    def test_ticket_created_with_user(self, temp_folder):
        tombola_dao = TombolaDAO(temp_folder)
        tombola = TombolaModel(
            1, datetime.fromisoformat("2000-01-01 00:00:00"), datetime.now()
        )
        tombola = tombola_dao.create(tombola.start_date, tombola.end_date)

        user_dao = UserDAO(temp_folder)
        user = UserModel(1, "test@test.test", "password", CityModel(1, "test", "1111"))
        user = user_dao.register(
            user.email, user.password, user.city.name, user.city.postal_code
        )

        ticket_dao = TicketDAO(temp_folder)
        ticket = TicketModel("abc", tombola, None, user)
        ticket = ticket_dao.create(ticket.code, ticket.tombola.id, None)
        ticket = ticket_dao.assign_user(ticket, user)

        assert ticket is not None
        assert ticket.user is not None
        assert ticket.user.id == user.id

    def test_ticket_created(self, temp_folder):
        tombola_dao = TombolaDAO(temp_folder)
        tombola = TombolaModel(
            1, datetime.fromisoformat("2000-01-01 00:00:00"), datetime.now()
        )
        tombola = tombola_dao.create(tombola.start_date, tombola.end_date)

        prize_dao = PrizeDAO(temp_folder)
        prize = PrizeModel(1, tombola, "test", 100, 0)
        prize = prize_dao.create(
            prize.tombola.id, prize.description, prize.nb_available
        )

        user_dao = UserDAO(temp_folder)
        user = UserModel(1, "test@test.test", "password", CityModel(1, "test", "1111"))
        user = user_dao.register(
            user.email, user.password, user.city.name, user.city.postal_code
        )

        ticket_dao = TicketDAO(temp_folder)
        ticket = TicketModel("abc", tombola, prize, user)
        ticket = ticket_dao.create(
            ticket.code, ticket.tombola.id, ticket.prize.id if ticket.prize else None
        )
        ticket = ticket_dao.assign_user(ticket, user)

        assert ticket is not None
        assert ticket.prize is not None
        assert ticket.user is not None
