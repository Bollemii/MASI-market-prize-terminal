import pytest

from src.dataaccess.dao.user_dao import UserDAO
from src.dataaccess.dao.city_dao import CityDAO
from src.dataaccess.repository.user_repository import UserRepository
from src.dataaccess.repository.city_repository import CityRepository
from src.utils.password_manager import PasswordManager
from src.dataaccess.entity.user_entity import UserEntity
from src.model.user_model import UserModel
from src.dataaccess.entity.city_entity import CityEntity
from src.model.city_model import CityModel


class TestUserIntegration:
    @pytest.fixture(scope="function", autouse=True, name="temp_folder")
    def create_temporary_testfolder(
        self, tmp_path_factory: pytest.TempPathFactory
    ) -> str:
        base_path = "test_user_repository"
        return str(tmp_path_factory.mktemp(base_path, True))

    @pytest.fixture(scope="function", autouse=True, name="user_repository")
    def create_user_repository(self, temp_folder: str) -> UserRepository:
        password_manager = PasswordManager()
        city_repository = CityRepository(temp_folder)
        return UserRepository(temp_folder, city_repository, password_manager)

    @pytest.fixture(scope="function", autouse=True, name="user_dao")
    def create_user_dao(self, temp_folder: str) -> UserDAO:
        password_manager = PasswordManager()
        city_repository = CityRepository(temp_folder)
        user_repository = UserRepository(temp_folder, city_repository, password_manager)
        city_dao = CityDAO(city_repository)
        return UserDAO(user_repository, city_dao)

    def test_register_from_repository(self, user_repository: UserRepository):
        city = CityEntity(1, "Bruxelles", "1000")
        user = UserEntity(1, "test@test.be", "password", city)

        result = user_repository.register(
            user.email, user.password, user.city.name, user.city.postal_code
        )

        password_manager = PasswordManager()

        assert result.email == user.email
        assert password_manager.check_password(user.password, result.password)
        assert result.city.name == user.city.name
        assert result.city.postal_code == user.city.postal_code
        assert result.is_tenant == user.is_tenant

    def test_register_from_dao(self, user_dao: UserDAO):
        city = CityModel(1, "Bruxelles", "1000")
        user = UserModel(1, "test@test.be", "password", city)

        result = user_dao.register(
            user.email, user.password, user.city.name, user.city.postal_code
        )

        password_manager = PasswordManager()

        assert result.email == user.email
        assert password_manager.check_password(user.password, result.password)
        assert result.city.name == user.city.name
        assert result.city.postal_code == user.city.postal_code
        assert result.is_tenant == user.is_tenant
