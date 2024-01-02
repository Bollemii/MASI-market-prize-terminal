import os

from src.controllers.connection_controller import ConnectionController
from src.controllers.play_ticket_controller import PlayTicketController
from src.controllers.register_controller import RegisterController
from src.controllers.create_tombola_controller import CreateTombolaController
from src.controllers.get_ticket_controller import GetTicketController
from src.views.home import Home


class Application:
    @staticmethod
    def run():
        base_path = os.path.join(os.getcwd(), "data")

        Application._prepare(base_path)

        Home(
            RegisterController(base_path),
            ConnectionController(base_path),
            CreateTombolaController(base_path),
            PlayTicketController(base_path),
            GetTicketController(base_path),
        ).show()

    @staticmethod
    def _prepare(base_path: str):
        os.makedirs(base_path, exist_ok=True)
