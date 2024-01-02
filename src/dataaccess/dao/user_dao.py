from src.model.user_model import UserModel
from src.dataaccess.entity.user_entity import UserEntity
from src.dataaccess.repository.user_repository import UserRepository
from src.dataaccess.dao.city_dao import CityDAO
from src.exception.user_not_found_exception import UserNotFoundException


class UserDAO:
    def __init__(self, base_path: str):
        self.user_repository = UserRepository(base_path)
        self.city_dao = CityDAO(base_path)

    def convert_user_entity_to_user_model(self, entity: UserEntity) -> UserModel:
        return UserModel(
            entity.id,
            entity.email,
            entity.password,
            self.city_dao.convert_city_entity_to_city_model(entity.city),
            entity.is_tenant,
        )

    def connection(self, email: str, password: str) -> UserModel:
        entity = self.user_repository.connection(email, password)
        if entity is None:
            raise UserNotFoundException()
        return self.convert_user_entity_to_user_model(entity)

    def register(
        self, email: str, password: str, city_name: str, postal_code: str
    ) -> UserModel:
        entity = self.user_repository.register(email, password, city_name, postal_code)
        return self.convert_user_entity_to_user_model(entity)

    def update(self, user: UserModel, email: str, password: str) -> UserModel:
        entity = self.user_repository.update(user.id, email, password)
        return self.convert_user_entity_to_user_model(entity)
