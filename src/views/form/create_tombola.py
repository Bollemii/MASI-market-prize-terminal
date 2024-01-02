from src.views.generics.menu import Form
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
        total_prizes = 0

        is_more = True
        print("Obtention des lots")
        while is_more:
            print("------------------")
            prize = self._get_prize()
            total_prizes += prize.nb_available
            prizes.append(prize)
            is_more = self._get_continue()

        nb_tickets = -1
        while nb_tickets < total_prizes:
            nb_tickets = self._get_number(
                f"Entrez le nombre de tickets à générer (minimum {total_prizes}) : "
            )
        tombola = self.create_tombola_controller.create_tombola(
            start_date, end_date, prizes, nb_tickets
        )

        # Print all codes tickets to test the application and play ticket feature
        tickets = self.get_ticket_controller.get_ticket_by_tombola(tombola.id)
        for ticket in tickets:
            print(ticket.code)

        self._prompt_user(
            "Tombola créée avec succès (appuyez sur entrée pour continuer)"
        )

    def _get_prize(self) -> PrizeModel:
        prize_description = self._prompt_user("Entrez la description du lot : ")
        prize_quantity = self._get_number("Entrez la quantité de lots à gagner : ")

        prize = PrizeModel(None, None, prize_description, prize_quantity)

        return prize

    def _get_continue(self) -> bool:
        response = ""
        while response not in ["y", "n"]:
            response = self._prompt_user(
                "Voulez-vous ajouter un nouveau lot ? (y/n) : "
            )
        return response == "y"
