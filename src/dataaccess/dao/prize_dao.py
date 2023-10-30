from dataaccess.entity.prize_entity import Prize as PrizeEntity
from models.prize import Prize


def convert_prize_entity_to_prize_model(entity: PrizeEntity) -> Prize:
    return Prize(
        id=entity.id,
        description=entity.description,
        nb_available=entity.nb_available,
        nb_won=entity.nb_won,
    )
