from src.dataaccess.dao.user_dao import UserDAO
from src.model.user import User


class RegisterController:
    def __init__(self, base_path: str):
        self.user_dao = UserDAO(base_path)

    def register(
        self,
        email: str,
        password: str,
        confirm_password: str,
        city_name: str,
        postal_code: str,
    ) -> User | None:
        if password != confirm_password:
            raise Exception("Passwords don't match")
        try:
            return self.user_dao.register(email, password, city_name, postal_code)
        except Exception as e:
            print(e)
            return None
