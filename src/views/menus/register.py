from consolemenu.prompt_utils import UserQuit

from src.exceptions.password_exception import PasswordException
from src.views.generics.menu import Form, Menu
from src.controllers.iregister_controller import IRegisterController


class Register(Form):
    def __init__(self, parent_menu: Menu, register_controller: IRegisterController):
        super().__init__(parent_menu)
        self.register_controller = register_controller

    def execute(self):
        try:
            print("Formulaire d'enregistrement\n")
            email = self._prompt_email("Entrez votre email : ", enable_quit=True)
            password = self._prompt_password("Entrez votre mot de passe : ")
            confirm_password = self._prompt_password("Confirmez votre mot de passe : ")
            postal_code = self._prompt_user("Entrez votre code postal : ")
            city_name = self._prompt_user("Entrez votre ville : ")

            user = self.register_controller.register(
                email, password, confirm_password, city_name, postal_code
            )

            self._prompt_to_continue("Vous êtes bien enregistré")
            return user
        except UserQuit:
            pass
        except PasswordException:
            self._prompt_to_continue("Les mots de passe ne correspondent pas")
            return None
        except Exception:
            self._prompt_to_continue("Erreur lors de l'enregistrement")
            return None
