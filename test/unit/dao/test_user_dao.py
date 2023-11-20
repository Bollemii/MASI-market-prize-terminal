import pytest

from src.dataaccess.entity.city_entity import CityEntity
from src.dataaccess.dao.user_dao import UserDAO
from src.dataaccess.entity.user_entity import UserEntity


class TestUserDAO:
    @pytest.fixture(scope="function", autouse=True, name="temp_folder")
    def create_temporary_testfolder(
        self, tmp_path_factory: pytest.TempPathFactory
    ) -> str:
        base_path = "test_user_dao"
        return str(tmp_path_factory.mktemp(base_path, True))

    def test_init(self, temp_folder):
        """Test init"""
        user_dao = UserDAO(temp_folder)

        assert user_dao.user_repository is not None
        assert user_dao.city_dao is not None

    def test_dao_converter(self, temp_folder):
        entity = UserEntity(
            id=1,
            email="test@test.com",
            password="password",
            city=CityEntity(1, "City", "1111"),
            is_tenant=False,
        )
        model = UserDAO(temp_folder).convert_user_entity_to_user_model(entity)
        assert model.email == entity.email
        assert model.password == entity.password
        assert model.city.name == entity.city.name
        assert model.city.postal_code == entity.city.postal_code
        assert model.is_tenant == entity.is_tenant
