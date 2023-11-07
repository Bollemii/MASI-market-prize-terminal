from src.dataaccess.dao.user_dao import UserDAO


class RegisterController:
    def __init__(self):
        self.user_dao = UserDAO()

    def register(
        self,
        email: str,
        password: str,
        confirm_password: str,
        city_name: str,
        postal_code: str,
    ):
        if password != confirm_password:
            raise Exception("Passwords don't match")
        return self.user_dao.register(email, password, city_name, postal_code)
