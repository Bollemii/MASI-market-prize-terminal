from dataaccess.dao import user_dao
from dataaccess.dao import prize_dao

from dataaccess.entity.ticket_entity import Ticket as TicketEntity
from models.ticket import Ticket
from models.user import User


def convert_ticket_entity_to_ticket_model(entity: TicketEntity) -> Ticket:
    return Ticket(
        code=entity.code,
        prize=prize_dao.convert_prize_entity_to_prize_model(entity.prize)
        if entity.prize is not None
        else None,
        user=user_dao.convert_user_entity_to_user_model(entity.user)
        if entity.user is not None
        else None,
    )


def get_by_code(code: str) -> "Ticket":
    entity = TicketEntity.get_by_code(code)
    return convert_ticket_entity_to_ticket_model(entity)


def assign_user(ticket: Ticket, user: User) -> Ticket:
    entity = TicketEntity.assign_user(ticket.code, user.id)
    return convert_ticket_entity_to_ticket_model(entity)
