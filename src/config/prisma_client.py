from prisma import Prisma
import atexit

db = Prisma()

db.connect()


def close_db():
    db.disconnect()


atexit.register(close_db)
