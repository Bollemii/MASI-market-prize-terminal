from src.dataaccess.dao.iuser_dao import IUserDAO
from src.models.user_model import UserModel
from src.dataaccess.entities.user_entity import UserEntity
from src.dataaccess.repositories.iuser_repository import IUserRepository
from src.dataaccess.dao.icity_dao import ICityDAO
from src.exceptions.user_not_found_exception import UserNotFoundException


class UserDAO(IUserDAO):
    """Dao for User"""

    def __init__(self, user_repository: IUserRepository, city_dao: ICityDAO):
        self.user_repository = user_repository
        self.city_dao = city_dao

    def convert_user_entity_to_user_model(self, entity: UserEntity) -> UserModel:
        """Convert user entity to user model"""
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

    def update(
        self, user: UserModel, email: str | None = None, password: str | None = None
    ) -> UserModel:
        entity = None
        if email is not None:
            entity = self.user_repository.update_email(user.id, email)
        elif password is not None:
            entity = self.user_repository.update_password(user.id, password)

        if entity is None:
            raise Exception("User not updated")
        return self.convert_user_entity_to_user_model(entity)
