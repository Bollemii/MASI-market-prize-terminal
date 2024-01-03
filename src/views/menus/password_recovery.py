from src.controllers.iget_user_by_email_controller import IGetUserByEmailController
from src.controllers.iis_tenant_password_controller import IIsTenantPasswordController
from src.controllers.iupdate_password_account_controller import (
    IUpdatePasswordAccountController,
)
from src.exceptions.password_exception import PasswordException
from src.exceptions.user_not_found_exception import UserNotFoundException
from src.views.generics.form import Form
from src.views.generics.menu import Menu


class PasswordRecovery(Form):
    """Password recovery form"""

    def __init__(
        self,
        parent_menu: Menu,
        get_user_by_email_controller: IGetUserByEmailController,
        is_tenant_password_controller: IIsTenantPasswordController,
        update_password_controller: IUpdatePasswordAccountController,
    ):
        super().__init__(parent_menu)
        self.get_user_by_email_controller = get_user_by_email_controller
        self.is_tenant_password_controller = is_tenant_password_controller
        self.update_password_controller = update_password_controller

    def execute(self):
        try:
            print("Récupération de mot de passe\n")
            email = self._prompt_user("Veuillez entrer votre adresse email : ")
            user = self.get_user_by_email_controller.get_by_email(email)

            print(
                "\nAfin de vérifier votre identitén veuillez contacter le responsable de la boutique.\n"
            )
            tenant_password = self._prompt_password(
                "Code d'intervention du responsable : "
            )
            if not self.is_tenant_password_controller.check_password(tenant_password):
                self._prompt_to_continue("Code d'intervention incorrect")
                return

            password = self._prompt_password(
                "Veuillez entrer votre nouveau mot de passe : "
            )
            password_confirm = self._prompt_password(
                "Veuillez confirmer votre nouveau mot de passe : "
            )
            self.update_password_controller.update_password(
                user, password, password_confirm
            )

            self._prompt_to_continue("Votre mot de passe a bien été modifié")
        except UserNotFoundException:
            self._prompt_to_continue(
                "Aucun utilisateur n'a été trouvé avec cette adresse email"
            )
        except PasswordException:
            self._prompt_to_continue("Les mots de passe ne correspondent pas")
        except Exception:
            self._prompt_to_continue("Une erreur inconnue est survenue")
