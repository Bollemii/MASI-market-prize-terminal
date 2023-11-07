import os

from src.controllers.connection_controller import ConnectionController
from src.controllers.register_controller import RegisterController


class Application:
    def __init__(self):
        pass

    def run(self):
        print("Startup")
        base_path = os.path.join(os.getcwd(), "data")
        Application._prepare(base_path)

        ConnectionController(base_path)
        RegisterController(base_path)

    @staticmethod
    def _prepare(base_path: str):
        print("Prepare")
        os.makedirs(base_path, exist_ok=True)
