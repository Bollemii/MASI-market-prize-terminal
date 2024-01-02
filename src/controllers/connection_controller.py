from src.dataaccess.dao.iuser_dao import IUserDAO
from src.model.user_model import UserModel


class ConnectionController:
    def __init__(self, user_dao: IUserDAO):
        self.user_dao = user_dao

    def connection(self, email: str, password: str) -> UserModel:
        return self.user_dao.connection(email, password)
