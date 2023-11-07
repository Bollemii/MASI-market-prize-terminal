import sqlite3
import logging

logger = logging.getLogger(__name__)

user_table_ddl = """
CREATE TABLE "User" (
    "id" INTEGER NOT NULL PRIMARY KEY AUTOINCREMENT,
    "email" TEXT NOT NULL,
    "passwrord" TEXT NOT NULL,
    "is_tenant" BOOLEAN NOT NULL,
    "created" DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP,
    "updated" DATETIME NOT NULL
);
"""

city_table_ddl = """
CREATE TABLE "City" (
    "id" INTEGER NOT NULL PRIMARY KEY AUTOINCREMENT,
    "name" TEXT NOT NULL,
    "postal_code" INTEGER NOT NULL
);"""


ticket_table_ddl = """
CREATE TABLE "Ticket" (
    "code" TEXT NOT NULL PRIMARY KEY,
    "tombolaId" INTEGER NOT NULL,
    CONSTRAINT "Ticket_tombolaId_fkey" FOREIGN KEY ("tombolaId") REFERENCES "Tombola" ("id") ON DELETE RESTRICT ON UPDATE CASCADE
);
"""

tombola_table_ddl = """
CREATE TABLE "Tombola" (
    "id" INTEGER NOT NULL PRIMARY KEY AUTOINCREMENT,
    "name" TEXT NOT NULL,
    "created" DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP,
    "updated" DATETIME NOT NULL
);
"""

tombola_prize_table_ddl = """
CREATE TABLE "Tombola_Prize" (
    "id" INTEGER NOT NULL PRIMARY KEY AUTOINCREMENT,
    "tombolaId" INTEGER NOT NULL,
    "prizeId" INTEGER NOT NULL,
    "created" DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP,
    "updated" DATETIME NOT NULL,
    CONSTRAINT "Tombola_Prize_tombolaId_fkey" FOREIGN KEY ("tombolaId") REFERENCES "Tombola" ("id") ON DELETE RESTRICT ON UPDATE CASCADE,
    CONSTRAINT "Tombola_Prize_prizeId_fkey" FOREIGN KEY ("prizeId") REFERENCES "Prize" ("id") ON DELETE RESTRICT ON UPDATE CASCADE
);
"""

prize_table_ddl = """
CREATE TABLE "Prize" (
    "id" INTEGER NOT NULL PRIMARY KEY AUTOINCREMENT,
    "description" TEXT NOT NULL
);
"""

user_table_index = """
CREATE UNIQUE INDEX "User_email_key" ON "User"("email");
"""


class Datalayer:
    def __init__(self):
        self.conn = sqlite3.connect("./database.db")
        self.cursor = self.conn.cursor()
        all_tables = self.cursor.execute(
            "SELECT name FROM sqlite_master WHERE type='table';"
        ).fetchall()
        if len(all_tables) == 0:
            try:
                logger.info("Creating tables")
                self.cursor.execute("begin")
                self.cursor.execute(user_table_ddl)
                self.cursor.execute(city_table_ddl)
                self.cursor.execute(ticket_table_ddl)
                self.cursor.execute(tombola_table_ddl)
                self.cursor.execute(tombola_prize_table_ddl)
                self.cursor.execute(prize_table_ddl)
                self.cursor.execute(user_table_index)
                self.cursor.execute("commit")
            except Exception as e:
                self.cursor.execute("rollback")
                raise e

    def __new__(cls):
        if not hasattr(cls, "instance"):
            cls.instance = super(Datalayer, cls).__new__(cls)
        return cls.instance

    def get_cursor(self):
        return self.cursor


db = Datalayer()
