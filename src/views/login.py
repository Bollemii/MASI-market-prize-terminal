from src.views.menu import Form
from getpass import getpass
from src.controllers.connection_controller import ConnectionController


class Login(Form):
    def __init__(self, parent_menu, connection_controller: ConnectionController):
        super().__init__(parent_menu)
        self.connection_controller = connection_controller

    def execute(self):
        print("Formulaire de connexion")
        email = self._prompt_user("Entrez votre email : ")
        password = getpass("Entrez votre mot de passe : ")
        user = self.connection_controller.connection(email, password)
        if user is not None:
            input("Vous êtes bien connecté, appuyez sur entrée pour continuer")
        else:
            input("Erreur lors de la connexion, appuyez sur entrée pour continuer")
        return user
