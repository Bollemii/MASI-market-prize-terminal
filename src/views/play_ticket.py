from src.views.menu import Form
from src.controllers.play_ticket_controller import PlayTicketController
from src.model.user_model import UserModel
from src.views.animation import Slot
from src.utils.uuid_validator import uuid_validator
from time import sleep


class PlayTicket(Form):
    def __init__(
        self, parent_menu, play_ticket_controller: PlayTicketController, user: UserModel
    ):
        super().__init__(parent_menu)
        self.play_ticket_controller = play_ticket_controller
        self.user = user
        self.slot = Slot()

    def execute(self):
        ticket_code = self._prompt_user("Entrez le code de votre ticket")
        if not uuid_validator(ticket_code):
            print("Code de ticket invalide")
            return
        self.slot.start()
        result = self.play_ticket_controller.play_ticket(ticket_code, self.user)
        if not result:
            print("Code de ticket invalide")
            self.slot.stop(False)
            self.slot.join()
            self._prompt_user("Votre ticket n'existe pas ou a déjà été joué")
            return
        sleep(5)
        self.slot.stop(result.prize is not None)
        self.slot.join()
        if result.prize:
            self._prompt_user(f"Vous avez gagné {result.prize.description}")
        else:
            self._prompt_user("Vous n'avez rien gagné")
