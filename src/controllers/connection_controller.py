from src.dataaccess.dao.user_dao import UserDAO
from src.model.user_model import UserModel


class ConnectionController:
    def __init__(self, base_path: str):
        self.user_dao = UserDAO(base_path)

    def connection(self, email: str, password: str) -> UserModel:
        return self.user_dao.connection(email, password)
