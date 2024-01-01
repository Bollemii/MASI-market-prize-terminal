from src.views.menu import Menu
from src.views.register import Register
from src.views.create_tombola import CreateTombola
from consolemenu.items import FunctionItem, SubmenuItem
from src.controllers.register_controller import RegisterController
from src.controllers.connection_controller import ConnectionController
from src.controllers.create_tombola_controller import CreateTombolaController
from src.views.login import Login

class Home(Menu):
    def __init__(self, register_controller: RegisterController , connection_controller: ConnectionController, create_tombola_controller: CreateTombolaController):
        super().__init__("Loot borne", exit_option_text="Quitter")
        self.user_connected = None

        self.register_item = FunctionItem("S'enregistrer", Register(self, register_controller).execute)
        self.login_item = FunctionItem("Se connecter", Login(self, connection_controller).execute)
        self.create_tombola_item = FunctionItem("Créer une tombola", CreateTombola(self, create_tombola_controller).execute)
    
    def draw(self):
        if self.user_connected is None:
            self.user_connected = self.register_item.get_return() or self.login_item.get_return()
            if self.user_connected is not None:
                self.register_item = FunctionItem("S'enregistrer", Register(self, RegisterController).execute)
        self.items.clear()
        if self.user_connected is None:
            # Not logged in
            self.append_item(self.login_item)
            self.append_item(self.register_item)
        else:
            if self.user_connected.is_tenant:
                self.append_item(self.create_tombola_item)
            else:
                self.append_item(self.create_tombola_item)

        super().draw()
        

