from src.dataaccess.repositories.common.sqlite_repository import SqliteRepository
from src.dataaccess.repositories.itombola_repository import ITombolaRepository
from src.dataaccess.repositories.iuser_repository import IUserRepository
from src.dataaccess.repositories.iprize_repository import IPrizeRepository
from src.dataaccess.entities.ticket_entity import TicketEntity
from src.exceptions.ticket_not_found_exception import TicketNotFoundException
from src.exceptions.tombola_not_found_exception import TombolaNotFoundException
from src.dataaccess.repositories.iticket_repository import ITicketRepository


class TicketRepository(SqliteRepository, ITicketRepository):
    """Ticket repository"""

    def __init__(
        self,
        base_path: str,
        tombola_repository: ITombolaRepository,
        user_repository: IUserRepository,
        prize_repository: IPrizeRepository,
    ):
        super().__init__(base_path)
        self.tombola_repository = tombola_repository
        self.user_repository = user_repository
        self.prize_repository = prize_repository

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

    def _create_entity(
        self, code: str, tombola_id: int, prize_id: int | None, user_id: int | None
    ) -> TicketEntity:
        tombola = self.tombola_repository.get_by_id(tombola_id)
        if tombola is None:
            raise TombolaNotFoundException()
        user = self.user_repository.get_by_id(user_id) if user_id else None
        prize = self.prize_repository.get_by_id(prize_id) if prize_id else None
        return TicketEntity(code, tombola, prize, user)

    def get_by_code(self, code: str) -> TicketEntity | None:
        result = self.execute_query("""SELECT * FROM ticket WHERE code = ?""", (code,))
        if len(result) == 0:
            return None
        code, tombola_id, user_id, prize_id = result[0]
        return self._create_entity(code, tombola_id, prize_id, user_id)

    def assign_user(self, code: str, user_id: int) -> TicketEntity:
        result = self.execute_statement(
            """UPDATE ticket SET user_id = ? WHERE code = ?""", (user_id, code)
        )
        if result is None or len(result) == 0:
            raise TicketNotFoundException()
        code, tombola_id, user_id, prize_id = result[0]
        return self._create_entity(code, tombola_id, prize_id, user_id)

    def assign_prize(self, code: str, prize_id: int) -> TicketEntity:
        result = self.execute_statement(
            """UPDATE ticket SET prize_id = ? WHERE code = ?""", (prize_id, code)
        )
        if result is None or len(result) == 0:
            raise TicketNotFoundException()
        code, tombola_id, user_id, prize_id = result[0]
        return self._create_entity(code, tombola_id, prize_id, user_id)

    def create(self, code: str, tombola_id: int, prize_id: int | None) -> TicketEntity:
        result = self.execute_statement(
            """INSERT INTO ticket (code, tombola_id, prize_id) VALUES (?, ?, ?)""",
            (code, tombola_id, prize_id),
        )
        if result is None or len(result) == 0:
            raise Exception("Ticket not created")
        code, tombola_id, user_id, prize_id = result[0]
        return self._create_entity(code, tombola_id, prize_id, user_id)

    def get_by_tombola(self, tombola_id: int) -> list[TicketEntity]:
        result = self.execute_query(
            """SELECT * FROM ticket WHERE tombola_id = ?""", (tombola_id,)
        )
        return [
            self._create_entity(code, tombola_id, prize_id, user_id)
            for code, tombola_id, user_id, prize_id in result
        ]
