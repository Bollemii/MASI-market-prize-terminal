import pytest
from datetime import datetime

from src.controllers.play_ticket_controller import PlayTicketController
from src.dataaccess.dao.tombola_dao import TombolaDAO
from src.dataaccess.dao.ticket_dao import TicketDAO
from src.dataaccess.dao.prize_dao import PrizeDAO
from src.dataaccess.dao.user_dao import UserDAO
from src.model.city_model import CityModel
from src.model.ticket_model import TicketModel
from src.model.prize_model import PrizeModel
from src.model.tombola_model import TombolaModel
from src.model.user_model import UserModel


class TestTicketPlaying:
    @pytest.fixture(scope="function", autouse=True, name="temp_folder")
    def create_temporary_testfolder(
        self, tmp_path_factory: pytest.TempPathFactory
    ) -> str:
        base_path = "test_ticket_playing"
        return str(tmp_path_factory.mktemp(base_path, True))

    def test_ticket_user_assigned(self, temp_folder):
        tombola_dao = TombolaDAO(temp_folder)
        tombola = TombolaModel(
            1, datetime.fromisoformat("2000-01-01 00:00:00"), datetime.now()
        )
        tombola = tombola_dao.create(tombola.start_date, tombola.end_date)

        ticket_dao = TicketDAO(temp_folder)
        ticket = TicketModel("abc", tombola, None, None)
        ticket = ticket_dao.create(ticket.code, ticket.tombola.id, None)

        user_dao = UserDAO(temp_folder)
        user = UserModel(1, "test@test.test", "password", CityModel(1, "test", "1111"))
        user = user_dao.register(
            user.email, user.password, user.city.name, user.city.postal_code
        )

        controller = PlayTicketController(temp_folder)
        ticket_played = controller.play_ticket(ticket.code, user)

        assert ticket_played is not None
        assert ticket_played.user is not None
        assert ticket_played.user.id == user.id

    def test_ticket_tombola_won(self, temp_folder):
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
        ticket = TicketModel("abc", tombola, None, None)
        ticket = ticket_dao.create(ticket.code, ticket.tombola.id, prize.id)

        user_dao = UserDAO(temp_folder)
        user = UserModel(1, "test@test.test", "password", CityModel(1, "test", "1111"))
        user = user_dao.register(
            user.email, user.password, user.city.name, user.city.postal_code
        )

        controller = PlayTicketController(temp_folder)
        ticket_played = controller.play_ticket(ticket.code, user)

        assert ticket_played is not None
        assert ticket.prize is not None and ticket_played.prize is not None
        assert ticket_played.prize.id == ticket.prize.id
        assert ticket_played.prize.nb_won == ticket.prize.nb_won + 1
        assert ticket_played.prize.nb_available == ticket.prize.nb_available - 1
