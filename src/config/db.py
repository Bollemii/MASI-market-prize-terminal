user_table_ddl = """
CREATE TABLE "User" (
    "id" INTEGER NOT NULL PRIMARY KEY AUTOINCREMENT,
    "email" TEXT NOT NULL UNIQUE,
    "password" TEXT NOT NULL,
    "is_tenant" BOOLEAN NOT NULL DEFAULT FALSE,
    "city_id" INTEGER NOT NULL,
    "created" DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP,
    "updated" DATETIME NOT NULL,
    CONSTRAINT "User_city_id_fkey" FOREIGN KEY ("city_id") REFERENCES "City" ("id") ON DELETE RESTRICT ON UPDATE CASCADE
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
    "tombola_id" INTEGER NOT NULL,
    "user_id" INTEGER,
    "prize_id" INTEGER,
    CONSTRAINT "Ticket_tombola_id_fkey" FOREIGN KEY ("tombola_id") REFERENCES "Tombola" ("id") ON DELETE RESTRICT ON UPDATE CASCADE
    CONSTRAINT "Ticket_user_id_fkey" FOREIGN KEY ("user_id") REFERENCES "User" ("id") ON DELETE RESTRICT ON UPDATE CASCADE
    CONSTRAINT "Ticket_prize_id_fkey" FOREIGN KEY ("prize_id") REFERENCES "Tombola_Prize" ("id") ON DELETE RESTRICT ON UPDATE CASCADE
);
"""

tombola_table_ddl = """
CREATE TABLE "Tombola" (
    "id" INTEGER NOT NULL PRIMARY KEY AUTOINCREMENT,
    "start_date" DATETIME NOT NULL,
    "end_date" DATETIME NOT NULL,
    "created" DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP,
    "updated" DATETIME NOT NULL
);
"""

tombola_prize_table_ddl = """
CREATE TABLE "Tombola_Prize" (
    "id" INTEGER NOT NULL PRIMARY KEY AUTOINCREMENT,
    "tombola_id" INTEGER NOT NULL,
    "prize_id" INTEGER NOT NULL,
    "nb_available" INTEGER NOT NULL,
    "nb_won" INTEGER NOT NULL DEFAULT 0,
    "created" DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP,
    "updated" DATETIME NOT NULL,
    CONSTRAINT "Tombola_Prize_tombola_id_fkey" FOREIGN KEY ("tombola_id") REFERENCES "Tombola" ("id") ON DELETE RESTRICT ON UPDATE CASCADE,
    CONSTRAINT "Tombola_Prize_prize_id_fkey" FOREIGN KEY ("prize_id") REFERENCES "Prize" ("id") ON DELETE RESTRICT ON UPDATE CASCADE
);
"""

prize_table_ddl = """
CREATE TABLE "Prize" (
    "id" INTEGER NOT NULL PRIMARY KEY AUTOINCREMENT,
    "description" TEXT NOT NULL
);
"""
