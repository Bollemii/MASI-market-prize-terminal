from prisma import Prisma  # type: ignore
import bcrypt

from entity.city_entity import City


class User:
    id: int
    email: str
    passwrord: str
    city: City
    is_tenant: bool

    def __init__(
        self,
        id: int,
        email: str,
        password: str,
        city: str,
        postal_code: str,
        is_tenant: bool = False,
    ):
        self.id = id
        self.email = email
        self.password = password
        self.city = City(None, city, postal_code)
        self.is_tenant = is_tenant

    @staticmethod
    def update(id: int, email: str, password: str) -> "User":
        with Prisma() as db:
            return db.user.update(
                {
                    "where": {"id": id},
                    "data": {
                        "email": email,
                        "password": bcrypt.hashpw(
                            password.encode("utf-8"), bcrypt.gensalt()
                        ),
                    },
                }
            )

    @staticmethod
    def connection(email: str, password: str) -> "User":
        with Prisma() as db:
            user = db.user.find_first(
                where={"email": email},
            )
            if user is None:
                raise Exception("User not found")
            if not bcrypt.checkpw(password.encode("utf-8"), user.password):
                raise Exception("Password is incorrect")
            return user

    @staticmethod
    def register(
        email: str,
        password: str,
        city_name: str,
        postal_code: str,
    ) -> "User":
        with Prisma() as db:
            city: City = db.city.find_first(
                where={"postal_code": postal_code, "name": city_name}
            )
            if city is None:
                raise Exception("City not found")
            return db.user.create(
                {
                    "data": {
                        "email": email,
                        "password": bcrypt.hashpw(
                            password.encode("utf-8"), bcrypt.gensalt()
                        ),
                        "city": {"connect": {"id": city.id}},
                    }
                }
            )
