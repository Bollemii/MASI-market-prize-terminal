from uuid import UUID, uuid4


class UUIDManager:
    def generate(self):
        return str(uuid4())

    def validate(self, uuid_string):
        try:
            UUID(uuid_string, version=4)
        except ValueError:
            return False
        return True
