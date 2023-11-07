from src.model.city import City


class User:
    def __init__(
        self,
        id: int,
        email: str,
        password: str,
        city: City,
        is_tenant: bool = False,
    ):
        self.id = id
        self.email = email
        self.password = password
        self.city = city
        self.is_tenant = is_tenant
