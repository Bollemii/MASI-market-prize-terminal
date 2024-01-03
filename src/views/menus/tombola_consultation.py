from src.controllers.iget_tombola_state_controller import IGetTombolaStateController
from src.views.generics.form import Form
from src.models.tombola_model import TombolaModel
from src.views.generics.menu import Menu


class TombolaConsultation(Form):
    """Tombola consultation form"""

    def __init__(
        self,
        parent_menu: Menu,
        get_tombola_state_controller: IGetTombolaStateController,
    ):
        super().__init__(parent_menu)
        self.get_tombola_state_controller = get_tombola_state_controller

    def execute(self, tombola_model: TombolaModel):
        (
            tickets_played,
            tickets_remaining,
        ) = self.get_tombola_state_controller.get_tickets_state(tombola_model.id)
        prizes = self.get_tombola_state_controller.get_prizes_state(tombola_model.id)

        format = "%d/%m/%Y"
        print("Consultation de la tombola en cours\n")
        print(f"Date de début : {tombola_model.start_date.strftime(format)}")
        print(f"Date de fin : {tombola_model.end_date.strftime(format)}")
        print(f"Tickets : {tickets_played} joués - {tickets_remaining} restants")
        print("Lots :")
        for prize in prizes:
            print(
                f"    - {prize.description} : {prize.nb_won} remportés - {prize.nb_available} restants"
            )
        self._prompt_to_continue()
