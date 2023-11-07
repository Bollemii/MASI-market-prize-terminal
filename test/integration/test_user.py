import pytest

from src.dataaccess.dao.user_dao import UserDAO
from src.dataaccess.repository.user_repository import UserRepository

from src.dataaccess.entity.user_entity import User as UserEntity
from src.model.user import User as UserModel
from src.dataaccess.entity.city_entity import City as CityEntity
from src.model.city import City as CityModel


class TestUserIntegration:
    @pytest.fixture(scope="function", autouse=True, name="temp_folder")
    def create_temporary_testfolder(
        self, tmp_path_factory: pytest.TempPathFactory
    ) -> str:
        base_path = "test_user_repository"
        return str(tmp_path_factory.mktemp(base_path, True))

    def test_register_from_repository(self, temp_folder):
        city = CityEntity(1, "Bruxelles", "1000")
        user = UserEntity(1, "test@test.be", "password", city, True)

        user_repository = UserRepository(temp_folder)
        result = user_repository.register(
            user.email, user.password, user.city.name, user.city.postal_code
        )

        assert result.email == user.email
        assert result.password == user.password
        assert result.city.name == user.city.name
        assert result.city.postal_code == user.city.postal_code
        assert result.is_tenant == user.is_tenant

    def disabled_test_register_from_dao(self, temp_folder):
        city = CityModel(1, "Bruxelles", "1000")
        user = UserModel(1, "test@test.be", "password", city, True)

        user_dao = UserDAO(temp_folder)
        result = user_dao.register(
            user.email, user.password, user.city.name, user.city.postal_code
        )

        assert result.email == user.email
        assert result.password == user.password
        assert result.city.name == user.city.name
        assert result.city.postal_code == user.city.postal_code
        assert result.is_tenant == user.is_tenant
