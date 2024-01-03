from src.controllers.iupdate_password_account_controller import (
    IUpdatePasswordAccountController,
)
from src.dataaccess.dao.iuser_dao import IUserDAO
from src.exceptions.password_exception import PasswordException
from src.models.user_model import UserModel


class UpdatePasswordAccountController(IUpdatePasswordAccountController):
    """Controller for updating the user password"""

    def __init__(self, user_dao: IUserDAO):
        self.user_dao = user_dao

    def update_password(
        self, user: UserModel, password: str, confirm_password: str
    ) -> UserModel:
        if password != confirm_password:
            raise PasswordException("Passwords don't match")
        return self.user_dao.update(user, password=password)
