from src.controllers.iget_tombola_state_controller import IGetTombolaStateController
from src.dataaccess.dao.iprize_dao import IPrizeDAO
from src.dataaccess.dao.iticket_dao import ITicketDAO
from src.model.prize_model import PrizeModel


class GetTombolaStateController(IGetTombolaStateController):
    """Get tombola state controller"""

    def __init__(self, ticket_dao: ITicketDAO, prize_dao: IPrizeDAO):
        self.ticket_dao = ticket_dao
        self.prize_dao = prize_dao

    def get_tickets_state(self, tombola_id: int) -> tuple[int, int]:
        tickets = self.ticket_dao.get_by_tombola(tombola_id)
        tickets_played = 0
        for ticket in tickets:
            if ticket.user is not None:
                tickets_played += 1
        return tickets_played, len(tickets) - tickets_played

    def get_prizes_state(self, tombola_id: int) -> list[PrizeModel]:
        return self.prize_dao.get_by_tombola(tombola_id)
