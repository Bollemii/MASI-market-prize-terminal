from src.dataaccess.entity.prize_entity import PrizeEntity
from src.dataaccess.repository.sqlite_repository import SqliteRepository


class PrizeRepository(SqliteRepository):
    def __init__(self, base_path: str):
        super().__init__(base_path)

        self.execute_create_table(
            """
            CREATE TABLE "Prize" (
                "id" INTEGER NOT NULL PRIMARY KEY AUTOINCREMENT,
                "description" TEXT NOT NULL
            );
        """
        )
        self.execute_create_table(
            """
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
        )

    def get_by_id(self, id: int) -> PrizeEntity | None:
        result = self.execute_query(
            """
            SELECT id, prize.description, nb_available, nb_won FROM prize_tombola
            INNER JOIN prize ON prize.id = prize_tombola.prize_id
            WHERE prize_tombola.id = ?""",
            (id,),
        )
        if len(result) == 0:
            return None
        id, description, nb_available, nb_won = result[0]
        return PrizeEntity(id, description, nb_available, nb_won)
