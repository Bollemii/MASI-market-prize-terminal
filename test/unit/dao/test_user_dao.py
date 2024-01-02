import pytest

from src.dataaccess.dao.user_dao import UserDAO
from src.dataaccess.dao.city_dao import CityDAO
from src.dataaccess.entity.city_entity import CityEntity
from src.dataaccess.entity.user_entity import UserEntity
from src.dataaccess.repository.city_repository import CityRepository
from src.dataaccess.repository.user_repository import UserRepository
from src.utils.password_manager import PasswordManager


class TestUserDAO:
    @pytest.fixture(scope="function", autouse=True, name="temp_folder")
    def create_temporary_testfolder(
        self, tmp_path_factory: pytest.TempPathFactory
    ) -> str:
        base_path = "test_user_dao"
        return str(tmp_path_factory.mktemp(base_path, True))

    @pytest.fixture(scope="function", autouse=True, name="user_dao")
    def create_user_dao(self, temp_folder: str) -> UserDAO:
        password_manager = PasswordManager()
        city_repository = CityRepository(temp_folder)
        user_repository = UserRepository(temp_folder, city_repository, password_manager)

        city_dao = CityDAO(city_repository)

        return UserDAO(user_repository, city_dao)

    def test_init(self, user_dao: UserDAO):
        """Test init"""
        assert user_dao.user_repository is not None
        assert user_dao.city_dao is not None

    def test_dao_converter(self, user_dao: UserDAO):
        entity = UserEntity(
            id=1,
            email="test@test.com",
            password="password",
            city=CityEntity(1, "City", "1111"),
            is_tenant=False,
        )

        model = user_dao.convert_user_entity_to_user_model(entity)

        assert model.email == entity.email
        assert model.password == entity.password
        assert model.city.name == entity.city.name
        assert model.city.postal_code == entity.city.postal_code
        assert model.is_tenant == entity.is_tenant
