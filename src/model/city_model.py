class CityModel:
    """City model"""

    def __init__(self, id: int | None, name: str, postal_code: str):
        self.id = id
        self.name = name
        self.postal_code = postal_code
