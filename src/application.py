import os

from src.utils.uuid_manager import UUIDManager
from src.dataaccess.repository.city_repository import CityRepository
from src.dataaccess.repository.prize_repository import PrizeRepository
from src.dataaccess.repository.tombola_repository import TombolaRepository
from src.dataaccess.repository.ticket_repository import TicketRepository
from src.dataaccess.repository.user_repository import UserRepository
from src.dataaccess.dao.city_dao import CityDAO
from src.dataaccess.dao.prize_dao import PrizeDAO
from src.dataaccess.dao.tombola_dao import TombolaDAO
from src.dataaccess.dao.ticket_dao import TicketDAO
from src.dataaccess.dao.user_dao import UserDAO
from src.controllers.connection_controller import ConnectionController
from src.controllers.play_ticket_controller import PlayTicketController
from src.controllers.register_controller import RegisterController
from src.controllers.create_tombola_controller import CreateTombolaController
from src.controllers.get_ticket_controller import GetTicketController
from src.views.home import Home


class Application:
    def __init__(self):
        base_path = os.path.join(os.getcwd(), "data")
        os.makedirs(base_path, exist_ok=True)

        self.uuid_manager = UUIDManager()

        self.city_repository = CityRepository(base_path)
        self.prize_repository = PrizeRepository(base_path)
        self.tombola_repository = TombolaRepository(base_path)
        self.ticket_repository = TicketRepository(base_path)
        self.user_repository = UserRepository(base_path)

        self.city_dao = CityDAO(self.city_repository)
        self.tombola_dao = TombolaDAO(
            self.tombola_repository,
            self.prize_repository,
            self.ticket_repository,
            self.uuid_manager,
        )
        self.prize_dao = PrizeDAO(self.prize_repository, self.tombola_dao)
        self.user_dao = UserDAO(self.user_repository, self.city_dao)
        self.ticket_dao = TicketDAO(
            self.ticket_repository, self.tombola_dao, self.user_dao, self.prize_dao
        )

        self.register_controller = RegisterController(self.user_dao)
        self.connection_controller = ConnectionController(self.user_dao)
        self.create_tombola_controller = CreateTombolaController(self.tombola_dao)
        self.play_ticket_controller = PlayTicketController(
            self.ticket_dao, self.prize_dao
        )
        self.get_ticket_controller = GetTicketController(self.ticket_dao)

    def run(self):
        """Run the application"""
        Home(
            self.register_controller,
            self.connection_controller,
            self.create_tombola_controller,
            self.play_ticket_controller,
            self.get_ticket_controller,
        ).show()
