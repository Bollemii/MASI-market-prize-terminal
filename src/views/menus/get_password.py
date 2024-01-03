from getpass import getpass

from src.controllers.iconnection_controller import IConnectionController
from src.exceptions.user_not_found_exception import UserNotFoundException
from src.models.user_model import UserModel
from src.views.generics.form import Form
from src.views.generics.menu import Menu


class GetPassword(Form):
    """Get password form"""

    def __init__(self, parent_menu: Menu, connection_controller: IConnectionController):
        super().__init__(parent_menu)
        self.connection_controller = connection_controller

    def execute(self, user: UserModel):
        try:
            password = getpass("Entrez votre mot de passe : ")
            return self.connection_controller.connection(user.email, password)
        except UserNotFoundException:
            self._prompt_to_continue("Mot de passe incorrect")
            return None
        except Exception:
            self._prompt_to_continue("Une erreur inconnue est survenue")
            return None
