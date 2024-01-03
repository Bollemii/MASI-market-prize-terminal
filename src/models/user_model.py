from src.models.city_model import CityModel


class UserModel:
    """User model"""

    def __init__(
        self,
        id: int,
        email: str,
        password: str,
        city: CityModel,
        is_tenant: bool = False,
    ):
        self.id = id
        self.email = email
        self.password = password
        self.city = city
        self.is_tenant = is_tenant
