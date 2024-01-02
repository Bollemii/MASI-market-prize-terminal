from src.dataaccess.dao.user_dao import UserDAO
from src.model.user_model import UserModel


class ConnectionController:
    def __init__(self, user_dao: UserDAO):
        self.user_dao = user_dao

    def connection(self, email: str, password: str) -> UserModel:
        return self.user_dao.connection(email, password)
