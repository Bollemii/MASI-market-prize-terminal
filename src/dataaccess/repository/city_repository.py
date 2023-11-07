from src.dataaccess.repository.sqlite_repository import SqliteRepository
from src.dataaccess.entity.city_entity import City


class CityRepository:
    def __init__(self, base_path: str):
        self.repository = SqliteRepository(base_path)

    def get_by_id(self, id: int) -> City | None:
        result = self.repository.execute_query("SELECT * FROM city WHERE id = ?", (id,))
        if len(result) == 0:
            return None
        id, name, postal_code = result[0]
        return City(id, name, postal_code)

    def get_by_name_and_postal_code(self, name: str, postal_code: str) -> City | None:
        result = self.repository.execute_query(
            "SELECT * FROM city WHERE name = ? AND postal_code = ?", (name, postal_code)
        )
        if len(result) == 0:
            return None
        id, name, postal_code = result[0]
        return City(id, name, postal_code)

    def create(self, name: str, postal_code: str) -> City:
        result = self.repository.execute_statement(
            "INSERT INTO city (name, postal_code) VALUES (?, ?)", (name, postal_code)
        )
        if result is None or len(result) == 0:
            raise Exception("City not created")
        id, name, postal_code = result[0]
        return City(id, name, postal_code)
