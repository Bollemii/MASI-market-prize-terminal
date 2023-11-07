from prisma import Prisma  # type: ignore
from src.utils.password_manager import PasswordManager

from src.dataaccess.entity.user_entity import User
from src.dataaccess.entity.city_entity import City


class UserRepository:
    def __init__(self):
        self.password_manager = PasswordManager()

    def update(self, id: int, email: str, password: str) -> "User":
        with Prisma() as db:
            return db.user.update(
                {
                    "where": {"id": id},
                    "data": {
                        "email": email,
                        "password": self.password_manager.encrypt_password(password),
                    },
                }
            )

    def connection(self, email: str, password: str) -> "User" | None:
        with Prisma() as db:
            user = db.user.find_first(
                where={"email": email},
            )
            if user is None or not self.password_manager.check_password(
                password, user.password
            ):
                return None
            return user

    def register(
        self, email: str, password: str, city_name: str, postal_code: str
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
                        "password": self.password_manager.encrypt_password(password),
                        "city": {"connect": {"id": city.id}},
                    }
                }
            )
