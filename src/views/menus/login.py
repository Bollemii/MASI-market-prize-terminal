from getpass import getpass
from consolemenu.prompt_utils import UserQuit

from src.views.generics.menu import Form
from src.exceptions.user_not_found_exception import UserNotFoundException
from src.models.user_model import UserModel
from src.controllers.iconnection_controller import IConnectionController


class Login(Form):
    def __init__(self, parent_menu, connection_controller: IConnectionController):
        super().__init__(parent_menu)
        self.connection_controller = connection_controller

    def execute(self) -> UserModel | None:
        try:
            print("Formulaire de connexion")
            email = self._prompt_email("Entrez votre email : ", enable_quit=True)
            password = getpass("Entrez votre mot de passe : ")

            user = self.connection_controller.connection(email, password)

            self._prompt_to_continue("Vous êtes bien connecté")
            return user
        except UserQuit:
            return None
        except UserNotFoundException:
            self._prompt_to_continue(
                "Erreur de connexion, email ou mot de passe incorrect"
            )
            return None
        except Exception as e:
            self._prompt_to_continue(f"Erreur inconnue lors de la connexion : {e}")
            return None
