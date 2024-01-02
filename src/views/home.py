from consolemenu.items import FunctionItem

from src.model.user_model import UserModel
from src.utils.iuuid_manager import IUUIDManager
from src.views.form.tombola_consultation import TombolaConsultation
from src.views.generics.menu import Menu
from src.views.form.register import Register
from src.views.form.create_tombola import CreateTombola
from src.views.form.play_ticket import PlayTicket
from src.views.form.login import Login
from src.controllers.iregister_controller import IRegisterController
from src.controllers.iconnection_controller import IConnectionController
from src.controllers.icreate_tombola_controller import ICreateTombolaController
from src.controllers.iplay_ticket_controller import IPlayTicketController
from src.controllers.iget_ticket_controller import IGetTicketController
from src.controllers.iget_current_tombola_controller import IGetCurrentTombolaController
from src.controllers.icheck_tombola_dates_controller import ICheckTombolaDatesController
from src.controllers.iget_tombola_state_controller import IGetTombolaStateController


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
        self.uuid_manager = uuid_manager

        self.register_menu = Register(self, register_controller)
        self.login_menu = Login(self, connection_controller)
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

        self.play_ticket_item: FunctionItem

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

    def _draw_tenant_menu(self):
        """Draw tenant menu"""
        if self.user_connected is not None and self.user_connected.is_tenant:
            if self.current_tombola is None:
                create_tombola_item = FunctionItem(
                    "Créer une tombola",
                    self.create_tombola_menu.execute,
                )
                self.append_item(create_tombola_item)
            else:
                consultation_item = FunctionItem(
                    "Consulter la tombola en cours",
                    self.tombola_consultation_menu.execute,
                    args=(self.current_tombola,),
                )
                self.append_item(consultation_item)

    def _draw_client_menu(self):
        """Draw client menu"""
        if self.user_connected is not None and not self.user_connected.is_tenant:
            if self.current_tombola is not None:
                play_ticket_item = FunctionItem(
                    "Jouer un ticket",
                    self.play_ticket_menu.execute,
                    args=(
                        self.user_connected,
                        self.current_tombola,
                    ),
                )
                self.append_item(play_ticket_item)
            else:
                print("Aucune tombola en cours")

    def draw(self):
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
