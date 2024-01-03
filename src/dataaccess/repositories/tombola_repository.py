from datetime import datetime

from src.dataaccess.entities.tombola_entity import TombolaEntity
from src.dataaccess.repositories.common.sqlite_repository import SqliteRepository
from src.dataaccess.repositories.itombola_repository import ITombolaRepository


class TombolaRepository(SqliteRepository, ITombolaRepository):
    """Tombola repository"""

    def __init__(self, base_path: str):
        super().__init__(base_path)
        self.execute_create_table(
            """
            CREATE TABLE IF NOT EXISTS tombola (
                "id" INTEGER NOT NULL PRIMARY KEY AUTOINCREMENT,
                "start_date" DATETIME NOT NULL,
                "end_date" DATETIME NOT NULL,
                "created" DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP,
                "updated" DATETIME NULL
            );
        """
        )

    def get_by_id(self, id: int) -> TombolaEntity | None:
        result = self.execute_query(
            """SELECT id, start_date, end_date FROM tombola WHERE id = ?""",
            (id,),
        )
        if len(result) == 0:
            return None
        id, start_date, end_date = result[0]
        return TombolaEntity(
            id, datetime.fromisoformat(start_date), datetime.fromisoformat(end_date)
        )

    def get_tombola_by_date(self, date: datetime) -> TombolaEntity | None:
        result = self.execute_query(
            """SELECT id, start_date, end_date FROM tombola WHERE start_date <= ? AND end_date >= ?""",
            (date.isoformat(), date.isoformat()),
        )
        if len(result) == 0:
            return None
        id, start_date, end_date = result[0]
        return TombolaEntity(
            id, datetime.fromisoformat(start_date), datetime.fromisoformat(end_date)
        )

    def create(self, start_date: datetime, end_date: datetime) -> TombolaEntity:
        if self.are_tombolas_in_dates_range(start_date, end_date):
            raise Exception("There is already a tombola in this period")

        result = self.execute_statement(
            """INSERT INTO tombola (start_date, end_date) VALUES (?, ?)""",
            (start_date.isoformat(), end_date.isoformat()),
        )
        if result is None or len(result) == 0:
            raise Exception("Tombola not created")
        id, start_date_str, end_date_str, _, _ = result[0]
        return TombolaEntity(
            id,
            datetime.fromisoformat(start_date_str),
            datetime.fromisoformat(end_date_str),
        )

    def are_tombolas_in_dates_range(
        self, start_date: datetime, end_date: datetime
    ) -> bool:
        result = self.execute_query(
            """SELECT id FROM tombola
            WHERE (? BETWEEN start_date AND end_date) OR (? BETWEEN start_date AND end_date)""",
            (start_date.isoformat(), end_date.isoformat()),
        )
        return len(result) > 0
