from src.dataaccess.entity.prize_entity import PrizeEntity
from src.dataaccess.repository.common.sqlite_repository import SqliteRepository
from src.dataaccess.repository.tombola_repository import TombolaRepository
from src.dataaccess.repository.iprize_repository import IPrizeRepository


class PrizeRepository(SqliteRepository, IPrizeRepository):
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
                "updated" DATETIME NULL,
                CONSTRAINT "Tombola_Prize_tombola_id_fkey" FOREIGN KEY ("tombola_id") REFERENCES "Tombola" ("id") ON DELETE RESTRICT ON UPDATE CASCADE,
                CONSTRAINT "Tombola_Prize_prize_id_fkey" FOREIGN KEY ("prize_id") REFERENCES "Prize" ("id") ON DELETE RESTRICT ON UPDATE CASCADE
            );
        """
        )

    def _create_entity(
        self, id: int, tombola_id: int, prize_id: int, nb_available: int, nb_won: int
    ) -> PrizeEntity:
        tombola = self.tombola_repository.get_by_id(tombola_id)
        if tombola is None:
            raise Exception("Tombola not found")
        description = self._get_prize_item_description_by_id(prize_id)
        if description is None:
            raise Exception("Prize item not found")
        return PrizeEntity(id, tombola, description, nb_available, nb_won)

    def _get_prize_item_id_by_description(self, description: str) -> int | None:
        result = self.execute_query(
            """
            SELECT id FROM prize WHERE description = ?""",
            (description,),
        )
        if len(result) == 0:
            return None
        return result[0][0]

    def _get_prize_item_description_by_id(self, id: int) -> str | None:
        result = self.execute_query(
            """
            SELECT description FROM prize WHERE id = ?""",
            (id,),
        )
        if len(result) == 0:
            return None
        return result[0][0]

    def get_by_id(self, id: int) -> PrizeEntity | None:
        result = self.execute_query(
            """
            SELECT * FROM tombola_prize WHERE id = ?""",
            (id,),
        )
        if len(result) == 0:
            return None
        id, tombola_id, prize_id, nb_available, nb_won, _, _ = result[0]
        return self._create_entity(id, tombola_id, prize_id, nb_available, nb_won)

    def get_by_tombola_id(self, tombola_id: int) -> list[PrizeEntity]:
        result = self.execute_query(
            """
            SELECT * FROM tombola_prize WHERE tombola_id = ?""",
            (tombola_id,),
        )
        return [
            self._create_entity(id, tombola_id, prize_id, nb_available, nb_won)
            for id, tombola_id, prize_id, nb_available, nb_won, _, _ in result
        ]

    def prize_won(self, id: int) -> PrizeEntity:
        result = self.execute_statement(
            """
            UPDATE tombola_prize SET nb_won = nb_won + 1,
                nb_available = nb_available - 1
                WHERE id = ?;
            """,
            (id,),
        )
        if result is None or len(result) == 0:
            raise Exception("Prize not found")
        id, tombola_id, prize_id, nb_available, nb_won, _, _ = result[0]
        return self._create_entity(id, tombola_id, prize_id, nb_available, nb_won)

    def create_prize_item(self, description: str) -> int:
        result = self.execute_statement(
            """
            INSERT INTO prize(description) VALUES (?);
            """,
            (description,),
        )
        if result is None or len(result) == 0:
            raise Exception("Prize item not created")
        id, _ = result[0]
        return id

    def create(self, tombola_id: int, description: str, quantity: int) -> PrizeEntity:
        prize_item_id = self._get_prize_item_id_by_description(description)
        if prize_item_id is None:
            prize_item_id = self.create_prize_item(description)
        result = self.execute_statement(
            """
            INSERT INTO tombola_prize(tombola_id, prize_id, nb_available) VALUES (?, ?, ?);
            """,
            (tombola_id, prize_item_id, quantity),
        )
        if result is None or len(result) == 0:
            raise Exception("Prize not created")
        id, tombola_id, prize_id, nb_available, nb_won, _, _ = result[0]
        return self._create_entity(id, tombola_id, prize_id, nb_available, nb_won)
