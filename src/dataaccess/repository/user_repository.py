from src.dataaccess.entity.city_entity import City
from src.utils.password_manager import PasswordManager
from src.dataaccess.repository.city_repository import CityRepository
from src.dataaccess.repository.sqlite_repository import SqliteRepository
from src.dataaccess.entity.user_entity import User


class UserRepository:
    def __init__(self, base_path: str):
        self.password_manager = PasswordManager()
        self.repository = SqliteRepository(base_path)
        self.city_repository = CityRepository(base_path)

    def update(self, id: int, email: str, password: str):
        result = self.repository.execute_statement(
            "UPDATE user SET email = ?, password = ? WHERE id = ?",
            (email, self.password_manager.encrypt_password(password), id),
        )
        if result is None or len(result) == 0:
            raise Exception("User not updated")
        id, email, password, city_id, is_tenant = result[0]
        city = self.city_repository.get_by_id(city_id)
        if city is None:
            raise Exception("City not found")
        return User(id, email, password, city, is_tenant)

    def connection(self, email: str, password: str) -> User | None:
        result = self.repository.execute_query(
            "SELECT * FROM user WHERE email = ? AND password = ?",
            (email, self.password_manager.encrypt_password(password)),
        )
        if len(result) == 0:
            return None
        id, email, password, city_id, is_tenant = result[0]
        city = self.city_repository.get_by_id(city_id)
        if city is None:
            raise Exception("City not found")
        return User(id, email, password, city, is_tenant)

    def register(
        self, email: str, password: str, city_name: str, postal_code: str
    ) -> User:
        city = self.city_repository.get_by_name_and_postal_code(city_name, postal_code)
        if city is None:
            city = self.city_repository.create(city_name, postal_code)

        result = self.repository.execute_statement(
            "INSERT INTO user (email, password, city_id) VALUES (?, ?, ?)",
            (email, self.password_manager.encrypt_password(password), city.id),
        )
        if result is None or len(result) == 0:
            raise Exception("User not created")
        id, email, password, city_id, is_tenant = result[0]
        return User(
            id, email, password, City(city_id, city_name, postal_code), is_tenant
        )
