from consolemenu.items import FunctionItem

from src.model.user_model import UserModel
from src.views.generics.menu import Menu
from src.views.form.register import Register
from src.views.form.create_tombola import CreateTombola
from src.views.form.play_ticket import PlayTicket
from src.views.form.login import Login
from src.controllers.register_controller import RegisterController
from src.controllers.connection_controller import ConnectionController
from src.controllers.create_tombola_controller import CreateTombolaController
from src.controllers.play_ticket_controller import PlayTicketController


class Home(Menu):
    def __init__(
        self,
        register_controller: RegisterController,
        connection_controller: ConnectionController,
        create_tombola_controller: CreateTombolaController,
        play_ticket_controller: PlayTicketController,
        get_ticket_controller,
    ):
        super().__init__("Loot borne", exit_option_text="Quitter")
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
