from src.controllers.iget_user_by_email_controller import IGetUserByEmailController
from src.dataaccess.dao.iuser_dao import IUserDAO
from src.models.user_model import UserModel


class GetUserByEmailController(IGetUserByEmailController):
    def __init__(self, user_dao: IUserDAO):
        self.user_dao = user_dao

    def get_by_email(self, email: str) -> UserModel:
        return self.user_dao.get_by_email(email)
