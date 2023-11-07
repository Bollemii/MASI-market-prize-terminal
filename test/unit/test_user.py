from src.dataaccess.entity.city_entity import City
from src.dataaccess.dao.user_dao import UserDAO
from src.dataaccess.entity.user_entity import User


class TestUserManagement:
    def test_dao_converter(self):
        entity = User(
            id=1,
            email="test@test.com",
            password="password",
            city=City(1, "City", "1111"),
            is_tenant=False,
        )
        model = UserDAO().convert_user_entity_to_user_model(entity)
        assert model.email == entity.email
        assert model.password == entity.password
        assert model.city.name == entity.city.name
        assert model.city.postal_code == entity.city.postal_code
        assert model.is_tenant == entity.is_tenant
