from src.controllers.iupdate_email_account_controller import (
    IUpdateEmailAccountController,
)
from src.dataaccess.dao.iuser_dao import IUserDAO
from src.models.user_model import UserModel


class UpdateEmailAccountController(IUpdateEmailAccountController):
    """Controller for updating the user email"""

    def __init__(self, user_dao: IUserDAO):
        self.user_dao = user_dao

    def update_email(self, user: UserModel, email: str) -> UserModel:
        return self.user_dao.update(user, email=email)
