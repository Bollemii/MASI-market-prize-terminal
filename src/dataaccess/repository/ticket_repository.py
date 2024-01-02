from src.dataaccess.repository.common.sqlite_repository import SqliteRepository
from src.dataaccess.repository.tombola_repository import TombolaRepository
from src.dataaccess.repository.user_repository import UserRepository
from src.dataaccess.repository.prize_repository import PrizeRepository
from src.dataaccess.entity.ticket_entity import TicketEntity


class TicketRepository(SqliteRepository):
    def __init__(self, base_path: str):
        super().__init__(base_path)
        self.tombola_repository = TombolaRepository(base_path)
        self.user_repository = UserRepository(base_path)
        self.prize_repository = PrizeRepository(base_path)

        self.execute_create_table(
            """
            CREATE TABLE IF NOT EXISTS ticket (
                "code" TEXT NOT NULL PRIMARY KEY,
                "tombola_id" INTEGER NOT NULL,
                "user_id" INTEGER,
                "prize_id" INTEGER,
                CONSTRAINT "Ticket_tombola_id_fkey" FOREIGN KEY ("tombola_id") REFERENCES "Tombola" ("id") ON DELETE RESTRICT ON UPDATE CASCADE
                CONSTRAINT "Ticket_user_id_fkey" FOREIGN KEY ("user_id") REFERENCES "User" ("id") ON DELETE RESTRICT ON UPDATE CASCADE
                CONSTRAINT "Ticket_prize_id_fkey" FOREIGN KEY ("prize_id") REFERENCES "Tombola_Prize" ("id") ON DELETE RESTRICT ON UPDATE CASCADE
            );
        """
        )

    def create_entity(
        self, code: str, tombola_id: int, prize_id: int | None, user_id: int | None
    ) -> TicketEntity:
        tombola = self.tombola_repository.get_by_id(tombola_id)
        if tombola is None:
            raise Exception("Tombola not found")
        user = self.user_repository.get_by_id(user_id) if user_id else None
        prize = self.prize_repository.get_by_id(prize_id) if prize_id else None
        return TicketEntity(code, tombola, prize, user)

    def get_by_code(self, code: str) -> TicketEntity | None:
        result = self.execute_query("""SELECT * FROM ticket WHERE code = ?""", (code,))
        if len(result) == 0:
            return None
        code, tombola_id, user_id, prize_id = result[0]
        return self.create_entity(code, tombola_id, prize_id, user_id)

    def assign_user(self, code: str, user_id: int) -> TicketEntity:
        result = self.execute_statement(
            """UPDATE ticket SET user_id = ? WHERE code = ?""", (user_id, code)
        )
        if result is None or len(result) == 0:
            raise Exception("Ticket not updated")
        code, tombola_id, user_id, prize_id = result[0]
        return self.create_entity(code, tombola_id, prize_id, user_id)

    def assign_prize(self, code: str, prize_id: int) -> TicketEntity:
        result = self.execute_statement(
            """UPDATE ticket SET prize_id = ? WHERE code = ?""", (prize_id, code)
        )
        if result is None or len(result) == 0:
            raise Exception("Ticket not updated")
        code, tombola_id, user_id, prize_id = result[0]
        return self.create_entity(code, tombola_id, prize_id, user_id)

    def create(self, code: str, tombola_id: int, prize_id: int | None) -> TicketEntity:
        result = self.execute_statement(
            """INSERT INTO ticket (code, tombola_id, prize_id) VALUES (?, ?, ?)""",
            (code, tombola_id, prize_id),
        )
        if result is None or len(result) == 0:
            raise Exception("Ticket not created")
        code, tombola_id, user_id, prize_id = result[0]
        return self.create_entity(code, tombola_id, prize_id, user_id)
    
    def get_by_tombola(self, tombola_id: int) -> [TicketEntity]:
        result = self.execute_query("""SELECT * FROM ticket WHERE tombola_id = ?""", (tombola_id,))
        return [self.create_entity(code, tombola_id, prize_id, user_id) for code, tombola_id, user_id, prize_id in result]