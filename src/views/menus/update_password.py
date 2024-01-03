from src.controllers.iupdate_password_account_controller import (
    IUpdatePasswordAccountController,
)
from src.exceptions.password_exception import PasswordException
from src.models.user_model import UserModel
from src.views.generics.form import Form
from src.views.generics.menu import Menu


class UpdatePassword(Form):
    """Update password form"""

    def __init__(
        self,
        parent_menu: Menu,
        update_password_controller: IUpdatePasswordAccountController,
    ):
        super().__init__(parent_menu)
        self.update_password_controller = update_password_controller

    def execute(self, user: UserModel):
        try:
            password = self._prompt_password("Entrez votre nouveau mot de passe : ")
            confirm_password = self._prompt_password(
                "Confirmez votre nouveau mot de passe : "
            )

            user = self.update_password_controller.update_password(
                user, password, confirm_password
            )

            self._prompt_to_continue("Votre mot de passe a bien été mis à jour")
            return user
        except PasswordException:
            self._prompt_to_continue("Les mots de passe ne correspondent pas")
            return None
        except Exception:
            self._prompt_to_continue("Une erreur inconnue est survenue")
            return None
