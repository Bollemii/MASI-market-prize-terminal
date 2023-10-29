from entity.user_entity import User as UserEntity
from models.user import User as User


def convert_user_entity_to_user_model(entity: UserEntity) -> User:
    return User(
        id=entity.id,
        email=entity.email,
        password=entity.password,
        city=entity.city.name,
        postal_code=entity.city.postal_code,
        is_tenant=entity.is_tenant,
    )


def connection(email: str, password: str) -> "User":
    entity = UserEntity.connection(email, password)
    return convert_user_entity_to_user_model(entity)


def register(email: str, password: str, city_name: str, postal_code: str) -> "User":
    entity = UserEntity.register(email, password, city_name, postal_code)
    return convert_user_entity_to_user_model(entity)


def update(user: User, email: str, password: str) -> "User":
    entity = UserEntity.update(user.id, email, password)
    return convert_user_entity_to_user_model(entity)
