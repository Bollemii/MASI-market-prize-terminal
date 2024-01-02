import bcrypt


class PasswordManager:
    def encrypt_password(self, password: str) -> str:
        return bcrypt.hashpw(password.encode("utf-8"), bcrypt.gensalt()).decode("utf-8")

    def check_password(self, password: str, hashed_password: str | bytes) -> bool:
        if isinstance(hashed_password, str):
            hashed_password = hashed_password.encode("utf-8")
        return bcrypt.checkpw(password.encode("utf-8"), hashed_password)
