from src.dataaccess.entity.prize_entity import PrizeEntity
from src.dataaccess.repository.sqlite_repository import SqliteRepository
from src.dataaccess.repository.tombola_repository import TombolaRepository


class PrizeRepository(SqliteRepository):
    def __init__(self, base_path: str):
        super().__init__(base_path)
        self.tombola_repository = TombolaRepository(base_path)

        self.execute_create_table(
            """
            CREATE TABLE IF NOT EXISTS prize (
                "id" INTEGER NOT NULL PRIMARY KEY AUTOINCREMENT,
                "description" TEXT NOT NULL
            );
        """
        )
        self.execute_create_table(
            """
            CREATE TABLE IF NOT EXISTS tombola_prize (
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
        )

    def create_entity(
        self, id: int, tombola_id: int, description: str, nb_available: int, nb_won: int
    ) -> PrizeEntity:
        tombola = self.tombola_repository.get_by_id(tombola_id)
        if tombola is None:
            raise Exception("Tombola not found")
        return PrizeEntity(id, tombola, description, nb_available, nb_won)

    def get_by_id(self, id: int) -> PrizeEntity | None:
        result = self.execute_query(
            """
            SELECT id, tombola_id, prize.description, nb_available, nb_won FROM prize_tombola
            INNER JOIN prize ON prize.id = prize_tombola.prize_id
            WHERE prize_tombola.id = ?""",
            (id,),
        )
        if len(result) == 0:
            return None
        id, tombola_id, description, nb_available, nb_won = result[0]
        return self.create_entity(id, tombola_id, description, nb_available, nb_won)

    def get_by_tombola_id(self, tombola_id: int) -> list[PrizeEntity]:
        result = self.execute_query(
            """
            SELECT id, tombola_id, prize.description, nb_available, nb_won FROM prize_tombola
            INNER JOIN prize ON prize.id = prize_tombola.prize_id
            WHERE prize_tombola.tombola_id = ?""",
            (tombola_id,),
        )
        return [
            self.create_entity(id, tombola_id, description, nb_available, nb_won)
            for id, tombola_id, description, nb_available, nb_won in result
        ]

    def get_by_tombola_and_description(
        self, tombola_id: int, description: str
    ) -> PrizeEntity:
        result = self.execute_query(
            """
            SELECT id, tombola_id, prize.description, nb_available, nb_won FROM prize_tombola
            INNER JOIN prize ON prize.id = prize_tombola.prize_id
            WHERE prize_tombola.tombola_id = ? AND prize.description = ?""",
            (tombola_id, description),
        )
        if len(result) == 0:
            raise Exception("Prize not found")
        id, tombola_id, description, nb_available, nb_won = result[0]
        return self.create_entity(id, tombola_id, description, nb_available, nb_won)

    def prize_won(self, id: int) -> PrizeEntity:
        result = self.execute_statement(
            """
            UPDATE prize_tombola SET nb_won = nb_won + 1,
                SET nb_available = nb_available - 1
                WHERE id = ?;
            """,
            (id,),
        )
        if result is None or len(result) == 0:
            raise Exception("Prize not found")
        id, tombola_id, description, nb_available, nb_won = result[0]
        return self.create_entity(id, tombola_id, description, nb_available, nb_won)
