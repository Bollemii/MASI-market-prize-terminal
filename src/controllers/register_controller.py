from src.controllers.iregister_controller import IRegisterController
from src.dataaccess.dao.iuser_dao import IUserDAO
from src.exceptions.password_exception import PasswordException
from src.models.user_model import UserModel


class RegisterController(IRegisterController):
    """Register controller"""

    def __init__(self, user_dao: IUserDAO):
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
