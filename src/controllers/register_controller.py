from src.dataaccess.dao.user_dao import UserDAO
from src.exception.password_exception import PasswordException
from src.model.user_model import UserModel


class RegisterController:
    def __init__(self, user_dao: UserDAO):
        self.user_dao = user_dao

    def register(
        self,
        email: str,
        password: str,
        confirm_password: str,
        city_name: str,
        postal_code: str,
    ) -> UserModel:
        if password != confirm_password:
            raise PasswordException("Passwords don't match")
        return self.user_dao.register(email, password, city_name, postal_code)
