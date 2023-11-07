from src.dataaccess.entity.user_entity import User as UserEntity
from src.dataaccess.repository.user_repository import UserRepository
from src.model.user import User as User
from city_dao import CityDAO


class UserDAO:
    def __init__(self):
        self.user_repository = UserRepository()
        self.city_dao = CityDAO()

    def convert_user_entity_to_user_model(self, entity: UserEntity) -> User:
        return User(
            id=entity.id,
            email=entity.email,
            password=entity.password,
            city=self.city_dao.convert_city_entity_to_city_model(entity.city),
            is_tenant=entity.is_tenant,
        )

    def connection(self, email: str, password: str) -> "User" | None:
        entity = self.user_repository.connection(email, password)
        if entity is None:
            return None
        return self.convert_user_entity_to_user_model(entity)

    def register(
        self, email: str, password: str, city_name: str, postal_code: str
    ) -> "User":
        entity = self.user_repository.register(email, password, city_name, postal_code)
        return self.convert_user_entity_to_user_model(entity)

    def update(self, user: User, email: str, password: str) -> "User":
        entity = self.user_repository.update(user.id, email, password)
        return self.convert_user_entity_to_user_model(entity)
