from consolemenu.items import FunctionItem
from src.controllers.iget_user_by_email_controller import IGetUserByEmailController
from src.controllers.iis_tenant_password_controller import IIsTenantPasswordController
from src.controllers.iupdate_email_account_controller import (
    IUpdateEmailAccountController,
)
from src.controllers.iupdate_password_account_controller import (
    IUpdatePasswordAccountController,
)

from src.models.user_model import UserModel
from src.utils.iuuid_manager import IUUIDManager
from src.views.generics.menu import Menu
from src.views.menus.password_recovery import PasswordRecovery
from src.views.menus.tombola_consultation import TombolaConsultation
from src.views.menus.register import Register
from src.views.menus.create_tombola import CreateTombola
from src.views.menus.play_ticket import PlayTicket
from src.views.menus.login import Login
from src.controllers.iregister_controller import IRegisterController
from src.controllers.iconnection_controller import IConnectionController
from src.controllers.icreate_tombola_controller import ICreateTombolaController
from src.controllers.iplay_ticket_controller import IPlayTicketController
from src.controllers.iget_ticket_controller import IGetTicketController
from src.controllers.iget_current_tombola_controller import IGetCurrentTombolaController
from src.controllers.icheck_tombola_dates_controller import ICheckTombolaDatesController
from src.controllers.iget_tombola_state_controller import IGetTombolaStateController
from src.views.menus.update_account import UpdateAccount


class Home(Menu):
    def __init__(
        self,
        register_controller: IRegisterController,
        connection_controller: IConnectionController,
        create_tombola_controller: ICreateTombolaController,
        play_ticket_controller: IPlayTicketController,
        get_ticket_controller: IGetTicketController,
        get_current_tombola_controller: IGetCurrentTombolaController,
        get_tombola_state_controller: IGetTombolaStateController,
        check_tombola_controller: ICheckTombolaDatesController,
        update_email_controller: IUpdateEmailAccountController,
        update_password_controller: IUpdatePasswordAccountController,
        get_user_by_email_controller: IGetUserByEmailController,
        is_tenant_password_controller: IIsTenantPasswordController,
        uuid_manager: IUUIDManager,
    ):
        super().__init__("Bienvenue sur la borne chanceuse", exit_option_text="Quitter")
        self.user_connected: UserModel | None = None
        self.register_controller = register_controller
        self.connection_controller = connection_controller
        self.create_tombola_controller = create_tombola_controller
        self.play_ticket_controller = play_ticket_controller
        self.get_ticket_controller = get_ticket_controller
        self.get_current_tombola_controller = get_current_tombola_controller
        self.get_tombola_state_controller = get_tombola_state_controller
        self.check_tombola_controller = check_tombola_controller
        self.update_email_controller = update_email_controller
        self.update_password_controller = update_password_controller
        self.get_user_by_email_controller = get_user_by_email_controller
        self.is_tenant_password_controller = is_tenant_password_controller
        self.uuid_manager = uuid_manager

        self.register_menu = Register(self, register_controller)
        self.login_menu = Login(self, connection_controller)
        self.password_recovery_menu = PasswordRecovery(
            self,
            get_user_by_email_controller,
            is_tenant_password_controller,
            update_password_controller,
        )
        self.create_tombola_menu = CreateTombola(
            self,
            create_tombola_controller,
            get_ticket_controller,
            check_tombola_controller,
        )
        self.play_ticket_menu = PlayTicket(
            self,
            play_ticket_controller,
            uuid_manager,
        )
        self.tombola_consultation_menu = TombolaConsultation(
            self,
            get_tombola_state_controller,
        )

        self.register_item = FunctionItem("S'enregistrer", self.register_menu.execute)
        self.login_item = FunctionItem("Se connecter", self.login_menu.execute)

    def _logout(self):
        """Logout user"""
        self.user_connected = None
        # recreate items to clear their get_return
        self.register_item = FunctionItem("S'enregistrer", self.register_menu.execute)
        self.login_item = FunctionItem("Se connecter", self.login_menu.execute)

    def _draw_connexion_menu(self):
        """Draw connexion menu"""
        if self.user_connected is None:
            self.append_item(self.login_item)
            self.append_item(self.register_item)
            self.add_form("Récupérer votre mot de passe", self.password_recovery_menu)

    def _draw_tenant_menu(self):
        """Draw tenant menu"""
        if self.user_connected is not None and self.user_connected.is_tenant:
            if self.current_tombola is None:
                self.add_form("Créer une tombola", self.create_tombola_menu)
            else:
                self.add_form(
                    "Consulter la tombola en cours",
                    self.tombola_consultation_menu,
                    args=(self.current_tombola,),
                )

            update_account_menu = UpdateAccount(
                self.user_connected,
                self.connection_controller,
                self.update_email_controller,
                self.update_password_controller,
            )
            self.add_submenu("Modifier votre compte", update_account_menu)

    def _draw_client_menu(self):
        """Draw client menu"""
        if self.user_connected is not None and not self.user_connected.is_tenant:
            if self.current_tombola is not None:
                self.add_form(
                    "Jouer un ticket",
                    self.play_ticket_menu,
                    args=(self.user_connected, self.current_tombola),
                )
            else:
                self.subtitle = "Aucune tombola en cours"

            update_account_menu = UpdateAccount(
                self.user_connected,
                self.connection_controller,
                self.update_email_controller,
                self.update_password_controller,
            )
            self.add_submenu("Modifier votre compte", update_account_menu)

    def draw(self):
        self.subtitle = None

        if self.user_connected is None:
            self.user_connected = (
                self.register_item.get_return() or self.login_item.get_return()
            )
        self.current_tombola = self.get_current_tombola_controller.get_current_tombola()

        self.items.clear()

        if self.user_connected is None:
            self._draw_connexion_menu()
        else:
            if self.user_connected.is_tenant:
                self._draw_tenant_menu()
            else:
                self._draw_client_menu()

            self.append_item(FunctionItem("Se déconnecter", self._logout))
        super().draw()
