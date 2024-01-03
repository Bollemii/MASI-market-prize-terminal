import sqlite3
from src.utils.password_manager import PasswordManager

password_manager = PasswordManager()
with sqlite3.connect("data/database.sqlite") as connection:
    c = connection.cursor()

    c.execute(
        """
        CREATE TABLE IF NOT EXISTS city (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT NOT NULL,
            postal_code TEXT NOT NULL
        );"""
    )
    c.execute(
        """INSERT INTO city (name, postal_code) VALUES (?, ?) RETURNING id;""",
        ("Paris", "75000"),
    )
    city_id = c.fetchone()[0]

    c.execute(
        """
        CREATE TABLE IF NOT EXISTS user (
            "id" INTEGER NOT NULL PRIMARY KEY AUTOINCREMENT,
            "email" TEXT NOT NULL UNIQUE,
            "password" TEXT NOT NULL,
            "city_id" INTEGER NOT NULL REFERENCES "City" ("id") ON DELETE RESTRICT ON UPDATE CASCADE,
            "is_tenant" BOOLEAN NOT NULL DEFAULT FALSE,
            "created" DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP,
            "updated" DATETIME NULL
        );"""
    )
    c.execute(
        """INSERT INTO user (email, password, city_id, is_tenant) VALUES (?,?,?,?);""",
        ("admin@adm.adm", password_manager.encrypt_password("admin"), city_id, True),
    )
    connection.commit()
