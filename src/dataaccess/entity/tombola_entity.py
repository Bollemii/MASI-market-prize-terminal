from datetime import datetime


class TombolaEntity:
    def __init__(self, id: int, start_date: datetime, end_date: datetime):
        self.id = id
        self.start_date = start_date
        self.end_date = end_date
