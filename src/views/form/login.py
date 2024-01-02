from src.exception.user_not_found_exception import UserNotFoundException
from src.model.user_model import UserModel
from src.views.generics.menu import Form
from getpass import getpass
from src.controllers.connection_controller import ConnectionController


class Login(Form):
    def __init__(self, parent_menu, connection_controller: ConnectionController):
        super().__init__(parent_menu)
        self.connection_controller = connection_controller

    def execute(self) -> UserModel | None:
        print("Formulaire de connexion")
        email = self._get_email("Entrez votre email : ", enable_quit=True)
        password = getpass("Entrez votre mot de passe : ")

        try:
            user = self.connection_controller.connection(email, password)

            input("Vous êtes bien connecté, appuyez sur entrée pour continuer")
            return user
        except UserNotFoundException:
            input("Erreur lors de la connexion, appuyez sur entrée pour continuer")
            return None
        except Exception as e:
            input(
                f"""Erreur inconnue lors de la connexion : {
                    e}, appuyez sur entrée pour continuer"""
            )
            return None
