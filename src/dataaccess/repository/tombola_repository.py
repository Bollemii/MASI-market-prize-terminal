from datetime import datetime

from src.dataaccess.entity.tombola_entity import TombolaEntity
from src.dataaccess.repository.sqlite_repository import SqliteRepository


class TombolaRepository(SqliteRepository):
    def __init__(self, base_path: str):
        super().__init__(base_path)

        self.execute_create_table(
            """
            CREATE TABLE IF NOT EXISTS tombola (
                "id" INTEGER NOT NULL PRIMARY KEY AUTOINCREMENT,
                "start_date" DATETIME NOT NULL,
                "end_date" DATETIME NOT NULL,
                "created" DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP,
                "updated" DATETIME NOT NULL
            );
        """
        )

    def get_by_id(self, id: int) -> TombolaEntity | None:
        result = self.execute_query(
            "SELECT id, start_date, end_date FROM tombola WHERE id = ?",
            (id,),
        )
        if len(result) == 0:
            return None
        id, start_date, end_date = result[0]
        return TombolaEntity(id, start_date, end_date)

    def get_current_tombola(self, current_date: datetime) -> TombolaEntity | None:
        result = self.execute_query(
            "SELECT id, start_date, end_date FROM tombola WHERE start_date <= ? AND end_date >= ?",
            (current_date, current_date),
        )
        if len(result) == 0:
            return None
        id, start_date, end_date = result[0]
        return TombolaEntity(id, start_date, end_date)
