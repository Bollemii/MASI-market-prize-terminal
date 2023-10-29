from prisma import Prisma
import bcrypt

class User:
    id: int
    email: str
    passwrord: str
    is_tenant: bool

    def update(self, email: str, password: str) -> 'User':
        with Prisma() as db:
            return db.user.update({"where": {"id": self.id}, "data": {"email": email, "password": bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt()).decode('utf-8')}})

    @staticmethod
    def connection(email: str, password: str) -> 'User':
        with Prisma() as db:
            return db.user.find_first(where={"email": email, "password": password})
        
    @staticmethod
    def register(email: str, password: str, confirm_password: str) -> 'User':
        if password != confirm_password:
            raise Exception("Password and confirm password must be same")
        with Prisma() as db:
            return db.user.create({"data": {"email": email, "password": bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt()).decode('utf-8')}})
