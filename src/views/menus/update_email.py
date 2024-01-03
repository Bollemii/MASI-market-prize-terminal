from src.controllers.iupdate_email_account_controller import (
    IUpdateEmailAccountController,
)
from src.models.user_model import UserModel
from src.views.generics.form import Form
from src.views.generics.menu import Menu


class UpdateEmail(Form):
    """Update email form"""

    def __init__(
        self, parent_menu: Menu, update_email_controller: IUpdateEmailAccountController
    ):
        super().__init__(parent_menu)
        self.update_email_controller = update_email_controller

    def execute(self, user: UserModel):
        try:
            email = self._prompt_email("Entrez votre nouvel email : ")
            user = self.update_email_controller.update_email(user, email)
            self._prompt_to_continue("Votre email a bien été mis à jour")
            return user
        except Exception:
            self._prompt_to_continue("Une erreur inconnue est survenue")
            return None
