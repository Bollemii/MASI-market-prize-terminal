from src.dataaccess.entity.city_entity import CityEntity


class UserEntity:
    """User entity"""

    def __init__(
        self,
        id: int,
        email: str,
        password: str,
        city: CityEntity,
        is_tenant: bool = False,
    ):
        self.id = id
        self.email = email
        self.password = password
        self.city = city
        self.is_tenant = is_tenant
