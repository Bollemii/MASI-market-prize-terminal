from src.views.menu import Form
from src.controllers.create_tombola_controller import CreateTombolaController
from src.controllers.get_ticket_controller import GetTicketController
from src.model.prize_model import PrizeModel


class CreateTombola(Form):
    def __init__(
        self,
        parent_menu,
        create_tombola_controller: CreateTombolaController,
        get_ticket_controller: GetTicketController,
    ):
        super().__init__(parent_menu)
        self.create_tombola_controller = create_tombola_controller
        self.get_ticket_controller = get_ticket_controller

    def execute(self):
        print("Formulaire de création de tombola")
        start_date = self._get_date("Entrez la date de début de la tombola")
        end_date = self._get_date("Entrez la date de fin de la tombola")
        prizes = []
        is_more = True
        print("Obtention des lots")
        while is_more:
            print("------------------")
            prize, is_more = self._get_prize()
            prizes.append(prize)
        nb_loser = self._get_number("Entrez le nombre de ticket perdant : ")
        tombola = self.create_tombola_controller.create_tombola(
            start_date, end_date, prizes, nb_loser
        )
        tickets = self.get_ticket_controller.get_ticket_by_tombola(tombola.id)
        for ticket in tickets:
            print(ticket.code)
        self._prompt_user(
            "Tombola créée avec succès (appuyez sur entrée pour continuer)"
        )

    def _get_prize(self) -> PrizeModel:
        prize_description = self._prompt_user("Entrez la description du lot : ")
        prize_quantity = self._get_number("Entrez la quantité de lot : ")
        prize = PrizeModel(None, None, prize_description, prize_quantity, 0)
        is_more = self._get_continue()

        return prize, is_more

    def _get_continue(self) -> bool:
        response = ""
        while response not in ["y", "n"]:
            response = self._prompt_user("Voulez-vous continuer ? (y/n) : ")
        return response == "y"
