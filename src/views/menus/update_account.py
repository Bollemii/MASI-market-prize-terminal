from src.controllers.iconnection_controller import IConnectionController
from src.controllers.iupdate_email_account_controller import (
    IUpdateEmailAccountController,
)
from src.controllers.iupdate_password_account_controller import (
    IUpdatePasswordAccountController,
)
from src.models.user_model import UserModel
from src.views.generics.menu import Menu
from src.views.menus.get_password import GetPassword
from src.views.menus.update_email import UpdateEmail
from src.views.menus.update_password import UpdatePassword


class UpdateAccount(Menu):
    """Update user account menu"""

    def __init__(
        self,
        user: UserModel,
        connection_controller: IConnectionController,
        update_email_controller: IUpdateEmailAccountController,
        update_password_controller: IUpdatePasswordAccountController,
    ):
        super().__init__("Mise à jour de votre compte", exit_option_text="Retour")
        self.user = user

        self.get_password = GetPassword(self, connection_controller)
        self.update_email_menu = UpdateEmail(self, update_email_controller)
        self.update_password_menu = UpdatePassword(self, update_password_controller)

        self.need_password = True

    def draw(self):
        self.items.clear()

        if self.need_password:
            user = self.get_password.execute(self.user)
            if user is None:
                self.exit()
                return
            self.screen.clear()
            self.need_password = False

        self.add_form("Modifier votre email", self.update_email_menu, args=(self.user,))
        self.add_form(
            "Modifier votre mot de passe", self.update_password_menu, args=(self.user,)
        )
        self.add_exit()
        super().draw()
