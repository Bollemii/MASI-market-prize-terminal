from src.exceptions.password_exception import PasswordException
from src.utils.ipassword_manager import IPasswordManager
from src.dataaccess.repositories.iuser_repository import IUserRepository
from src.dataaccess.repositories.icity_repository import ICityRepository
from src.dataaccess.repositories.common.sqlite_repository import SqliteRepository
from src.dataaccess.entities.user_entity import UserEntity


class UserRepository(SqliteRepository, IUserRepository):
    """Repository for User"""

    def __init__(
        self,
        base_path: str,
        city_repository: ICityRepository,
        password_manager: IPasswordManager,
    ):
        super().__init__(base_path)

        self.city_repository = city_repository
        self.password_manager = password_manager

        self.execute_create_table(
            """
            CREATE TABLE IF NOT EXISTS user (
                "id" INTEGER NOT NULL PRIMARY KEY AUTOINCREMENT,
                "email" TEXT NOT NULL UNIQUE,
                "password" TEXT NOT NULL,
                "city_id" INTEGER NOT NULL REFERENCES "City" ("id") ON DELETE RESTRICT ON UPDATE CASCADE,
                "is_tenant" BOOLEAN NOT NULL DEFAULT FALSE,
                "created_at" DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP,
                "updated_at" DATETIME NULL
            );
        """
        )

    def _create_entity(
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
        return self._create_entity(id, email, password, city_id, is_tenant)

    def get_by_email(self, email: str) -> UserEntity | None:
        result = self.execute_query("SELECT * FROM user WHERE email = ?", (email,))
        if len(result) == 0:
            return None
        if len(result) > 1:
            raise Exception("Multiple users found")
        id, email, password, city_id, is_tenant, _, _ = result[0]
        return self._create_entity(id, email, password, city_id, is_tenant)

    def update_email(self, id: int, email: str) -> UserEntity:
        result = self.execute_statement(
            "UPDATE user SET email = ? WHERE id = ?",
            (email, id),
        )
        if result is None or len(result) == 0:
            raise Exception("User not updated")
        id, email, password, city_id, is_tenant, _, _ = result[0]
        return self._create_entity(id, email, password, city_id, is_tenant)

    def update_password(self, id: int, password: str) -> UserEntity:
        result = self.execute_statement(
            "UPDATE user SET password = ? WHERE id = ?",
            (self.password_manager.encrypt_password(password), id),
        )
        if result is None or len(result) == 0:
            raise Exception("User not updated")
        id, email, password, city_id, is_tenant, _, _ = result[0]
        return self._create_entity(id, email, password, city_id, is_tenant)

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
            raise PasswordException("Password is incorrect")
        return self._create_entity(id, email, password, city_id, is_tenant)

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
        return self._create_entity(id, email, password, city_id, is_tenant)

    def check_tenant_password(self, password: str) -> bool:
        result = self.execute_query("SELECT password FROM user WHERE is_tenant = TRUE")
        if len(result) == 0:
            raise Exception("Tenant not found")
        if len(result) > 1:
            raise Exception("Multiple tenants found")
        encrypted_password = result[0][0]
        return self.password_manager.check_password(password, encrypted_password)
