from src.controllers.iis_tenant_password_controller import IIsTenantPasswordController
from src.dataaccess.dao.iuser_dao import IUserDAO


class IsTenantPasswordController(IIsTenantPasswordController):
    """Controller for checking if the tenant password is correct"""

    def __init__(self, user_dao: IUserDAO):
        self.user_dao = user_dao

    def check_password(self, password: str) -> bool:
        return self.user_dao.check_tenant_password(password)
