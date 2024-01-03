from datetime import datetime
from consolemenu.prompt_utils import UserQuit

from src.views.generics.menu import Form, Menu
from src.controllers.icreate_tombola_controller import ICreateTombolaController
from src.controllers.iget_ticket_controller import IGetTicketController
from src.controllers.icheck_tombola_dates_controller import ICheckTombolaDatesController
from src.models.prize_model import PrizeModel


class CreateTombola(Form):
    def __init__(
        self,
        parent_menu: Menu,
        create_tombola_controller: ICreateTombolaController,
        get_ticket_controller: IGetTicketController,
        check_tombola_controller: ICheckTombolaDatesController,
    ):
        super().__init__(parent_menu)
        self.create_tombola_controller = create_tombola_controller
        self.get_ticket_controller = get_ticket_controller
        self.check_tombola_controller = check_tombola_controller

    def execute(self):
        try:
            print("Formulaire de création de tombola")
            start_date = self._prompt_date(
                "Entrez la date de début de la tombola", enable_quit=True
            )
            end_date = self._prompt_date("Entrez la date de fin de la tombola")

            if start_date >= end_date:
                self._prompt_to_continue(
                    "La date de début doit être avant la date de fin"
                )
                return
            if start_date < datetime.now():
                self._prompt_to_continue(
                    "Vous ne pouvez pas créer une tombola dans le passé"
                )
                return
            if not self.check_tombola_controller.is_period_available(
                start_date, end_date
            ):
                self._prompt_to_continue("Il y a déjà une tombola dans cette période")
                return

            prizes = []
            total_prizes = 0

            print("Obtention des lots")
            want_more = True
            while want_more:
                print("------------------")
                prize = self._get_prize()
                total_prizes += prize.nb_available
                prizes.append(prize)
                want_more = self._prompt_to_stop_continue(
                    "Voulez-vous ajouter un nouveau lot ?"
                )

            nb_tickets = -1
            while nb_tickets < total_prizes:
                nb_tickets = self._prompt_number(
                    f"""Entrez le nombre de tickets à générer (minimum {
                        total_prizes}) : """,
                    positive=True,
                )

            print("Génération des tickets, veuillez patienter...")
            tombola = self.create_tombola_controller.create_tombola(
                start_date, end_date, prizes, nb_tickets
            )

            # Print all codes tickets to test the application and play ticket feature
            tickets = self.get_ticket_controller.get_ticket_by_tombola(tombola.id)
            for ticket in tickets:
                print(ticket.code)

            self._prompt_to_continue("La tombola a été créée avec succès")
        except UserQuit:
            pass
        except Exception as e:
            self._prompt_to_continue(f"Erreur inconnue lors de la connexion : {e}")

    def _get_prize(self) -> PrizeModel:
        prize_description = self._prompt_user("Entrez la description du lot : ")
        prize_quantity = self._prompt_number(
            "Entrez la quantité de lots à gagner : ", positive=True
        )

        prize = PrizeModel(None, None, prize_description, prize_quantity)

        return prize
