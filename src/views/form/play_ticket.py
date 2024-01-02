from consolemenu.prompt_utils import UserQuit
from time import sleep

from src.views.generics.menu import Form
from src.views.animation.animation import Slot
from src.controllers.iplay_ticket_controller import IPlayTicketController
from src.model.user_model import UserModel
from src.utils.iuuid_manager import IUUIDManager


class PlayTicket(Form):
    def __init__(
        self,
        parent_menu,
        play_ticket_controller: IPlayTicketController,
        uuid_manager: IUUIDManager,
    ):
        super().__init__(parent_menu)
        self.play_ticket_controller = play_ticket_controller
        self.uuid_manager = uuid_manager
        self.slot = Slot()

    def execute(self, user: UserModel):
        try:
            ticket_code = self._prompt_user(
                "Entrez le code de votre ticket", enable_quit=True
            )

            if not self.uuid_manager.is_uuid(ticket_code):
                print("Code de ticket invalide")
                return

            result = self.play_ticket_controller.play_ticket(ticket_code, user)
            if not result:
                print("Votre ticket n'existe pas ou a déjà été joué")
                self._prompt_to_continue()
                return

            self.slot.start()
            sleep(5)
            self.slot.stop(result.prize is not None)
            self.slot.join()

            if result.prize:
                print(f"Vous avez gagné {result.prize.description}")
            else:
                print("Vous n'avez rien gagné")
            self._prompt_to_continue()
        except UserQuit:
            pass
        except Exception as e:
            self._prompt_to_continue(f"Erreur inconnue lors de la connexion : {e}")
