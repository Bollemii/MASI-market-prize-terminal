from src.dataaccess.dao.user_dao import UserDAO
from src.exception.password_exception import PasswordException
from src.model.user_model import UserModel


class RegisterController:
    def __init__(self, base_path: str):
        self.user_dao = UserDAO(base_path)

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
