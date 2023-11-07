from src.dataaccess.dao.user_dao import UserDAO


class ConnectionController:
    def __init__(self):
        self.user_dao = UserDAO()

    def connection(self, email: str, password: str):
        return self.user_dao.connection(email, password)
