from src.views.generics.menu import Form
from getpass import getpass
from src.controllers.register_controller import RegisterController


class Register(Form):
    def __init__(self, parent_menu, register_controller: RegisterController):
        super().__init__(parent_menu)
        self.register_controller = register_controller

    def execute(self):
        print("Formulaire d'enregistrement")
        email = self._prompt_user("Entrez votre email : ", enable_quit=True)
        password = getpass("Entrez votre mot de passe : ")
        confirm_password = getpass("Confirmez votre mot de passe : ")
        postal_code = self._prompt_user("Entrez votre code postal : ")
        city_name = self._prompt_user("Entrez votre ville : ")

        user = self.register_controller.register(
            email, password, confirm_password, city_name, postal_code
        )

        if user is not None:
            input("Vous êtes bien enregistré, appuyez sur entrée pour continuer")
        else:
            input("Erreur lors de l'enregistrement, appuyez sur entrée pour continuer")

        return user
