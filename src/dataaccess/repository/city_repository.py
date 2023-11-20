from src.dataaccess.repository.common.sqlite_repository import SqliteRepository
from src.dataaccess.entity.city_entity import CityEntity


class CityRepository(SqliteRepository):
    def __init__(self, base_path: str):
        super().__init__(base_path)
        self.execute_create_table(
            """
            CREATE TABLE IF NOT EXISTS city (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                name TEXT NOT NULL,
                postal_code TEXT NOT NULL
            );
        """
        )

    def create_entity(self, id: int, name: str, postal_code: str) -> CityEntity:
        return CityEntity(id, name, postal_code)

    def get_by_id(self, id: int) -> CityEntity | None:
        result = self.execute_query("SELECT * FROM city WHERE id = ?", (id,))
        if len(result) == 0:
            return None
        id, name, postal_code = result[0]
        return self.create_entity(id, name, postal_code)

    def get_by_name_and_postal_code(
        self, name: str, postal_code: str
    ) -> CityEntity | None:
        result = self.execute_query(
            "SELECT * FROM city WHERE name = ? AND postal_code = ?", (name, postal_code)
        )
        if len(result) == 0:
            return None
        id, name, postal_code = result[0]
        return self.create_entity(id, name, postal_code)

    def create(self, name: str, postal_code: str) -> CityEntity:
        result = self.execute_statement(
            "INSERT INTO city (name, postal_code) VALUES (?, ?)", (name, postal_code)
        )
        if result is None or len(result) == 0:
            raise Exception("City not created")
        id, name, postal_code = result[0]
        return self.create_entity(id, name, postal_code)
