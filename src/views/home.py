from consolemenu.items import FunctionItem

from src.model.user_model import UserModel
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


class Home(Menu):
    def __init__(
        self,
        register_controller: IRegisterController,
        connection_controller: IConnectionController,
        create_tombola_controller: ICreateTombolaController,
        play_ticket_controller: IPlayTicketController,
        get_ticket_controller: IGetTicketController,
    ):
        super().__init__("Bienvenue sur la borne chanceuse", exit_option_text="Quitter")
        self.user_connected: UserModel | None = None
        self.register_controller = register_controller
        self.connection_controller = connection_controller
        self.create_tombola_controller = create_tombola_controller
        self.play_ticket_controller = play_ticket_controller
        self.get_ticket_controller = get_ticket_controller

        self.register_item = FunctionItem(
            "S'enregistrer", Register(self, register_controller).execute
        )
        self.login_item = FunctionItem(
            "Se connecter", Login(self, connection_controller).execute
        )
        self.create_tombola_item = FunctionItem(
            "Créer une tombola",
            CreateTombola(
                self, create_tombola_controller, get_ticket_controller
            ).execute,
        )

        self.play_ticket_item: FunctionItem

    def _logout(self):
        self.user_connected = None
        # recreate items to clear their get_return
        self.register_item = FunctionItem(
            "S'enregistrer", Register(self, self.register_controller).execute
        )
        self.login_item = FunctionItem(
            "Se connecter", Login(self, self.connection_controller).execute
        )

    def draw(self):
        if self.user_connected is None:
            self.user_connected = (
                self.register_item.get_return() or self.login_item.get_return()
            )

        self.items.clear()

        if self.user_connected is None:
            self.append_item(self.login_item)
            self.append_item(self.register_item)
        else:
            if self.user_connected.is_tenant:
                self.append_item(self.create_tombola_item)
            else:
                self.play_ticket_item = FunctionItem(
                    "Jouer un ticket",
                    PlayTicket(
                        self, self.play_ticket_controller, self.user_connected
                    ).execute,
                )
                self.append_item(self.play_ticket_item)

            self.append_item(FunctionItem("Se déconnecter", self._logout))
        super().draw()
