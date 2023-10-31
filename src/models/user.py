from dataaccess.dao import user_dao

from models.city import City


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

    def update(self, email: str, password: str) -> "User":
        return user_dao.update(self, email, password)

    @staticmethod
    def connection(email: str, password: str) -> "User":
        return user_dao.connection(email, password)

    @staticmethod
    def register(
        email: str,
        password: str,
        config_password: str,
        city_name: str,
        postal_code: str,
    ) -> "User":
        if password != config_password:
            raise Exception("Password is not match")
        return user_dao.register(email, password, city_name, postal_code)
