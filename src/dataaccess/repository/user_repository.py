from src.utils.password_manager import PasswordManager
from src.dataaccess.repository.city_repository import CityRepository
from src.dataaccess.repository.common.sqlite_repository import SqliteRepository
from src.dataaccess.entity.user_entity import UserEntity


class UserRepository(SqliteRepository):
    def __init__(self, base_path: str):
        super().__init__(base_path)

        self.password_manager = PasswordManager()
        self.city_repository = CityRepository(base_path)

        self.execute_create_table(
            """
            CREATE TABLE IF NOT EXISTS user (
                "id" INTEGER NOT NULL PRIMARY KEY AUTOINCREMENT,
                "email" TEXT NOT NULL UNIQUE,
                "password" TEXT NOT NULL,
                "city_id" INTEGER NOT NULL REFERENCES "City" ("id") ON DELETE RESTRICT ON UPDATE CASCADE,
                "is_tenant" BOOLEAN NOT NULL DEFAULT FALSE,
                "created" DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP,
                "updated" DATETIME NULL
            );
        """
        )

    def create_entity(
        self, id: int, email: str, password: str, city_id: int, is_tenant: bool
    ) -> UserEntity:
        city = self.city_repository.get_by_id(city_id)
        if city is None:
            raise Exception("City not found")
        return UserEntity(id, email, password, city, bool(is_tenant))

    def get_by_id(self, id: int) -> UserEntity | None:
        result = self.execute_query("SELECT * FROM user WHERE id = ?", (id,))
        if len(result) == 0:
            return None
        id, email, password, city_id, is_tenant, _, _ = result[0]
        return self.create_entity(id, email, password, city_id, is_tenant)

    def update(self, id: int, email: str, password: str):
        result = self.execute_statement(
            "UPDATE user SET email = ?, password = ? WHERE id = ?",
            (email, self.password_manager.encrypt_password(password), id),
        )
        if result is None or len(result) == 0:
            raise Exception("User not updated")
        id, email, password, city_id, is_tenant, _, _ = result[0]
        return self.create_entity(id, email, password, city_id, is_tenant)

    def connection(self, email: str, password: str) -> UserEntity | None:
        email = email.lower()
        result = self.execute_query(
            "SELECT * FROM user WHERE email = ?",
            (email,),
        )
        if len(result) == 0:
            return None
        id, email, encrypted_password, city_id, is_tenant, _, _ = result[0]
        if not self.password_manager.check_password(password, encrypted_password):
            return None
        return self.create_entity(id, email, password, city_id, is_tenant)

    def register(
        self, email: str, password: str, city_name: str, postal_code: str
    ) -> UserEntity:
        city = self.city_repository.get_by_name_and_postal_code(city_name, postal_code)
        if city is None:
            city = self.city_repository.create(city_name, postal_code)
        email = email.lower()
        result = self.execute_statement(
            "INSERT INTO user (email, password, city_id) VALUES (?, ?, ?)",
            (email, self.password_manager.encrypt_password(password), city.id),
        )
        if result is None or len(result) == 0:
            raise Exception("User not created")

        id, email, password, city_id, is_tenant, _, _ = result[0]
        return self.create_entity(id, email, password, city_id, is_tenant)
