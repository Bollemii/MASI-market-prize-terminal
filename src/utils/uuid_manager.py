from uuid import UUID, uuid4

from src.utils.iuuid_manager import IUUIDManager


class UUIDManager(IUUIDManager):
    """UUID Manager"""

    def generate(self) -> str:
        return str(uuid4())

    def is_uuid(self, uuid_string) -> bool:
        try:
            UUID(uuid_string, version=4)
            return True
        except ValueError:
            return False
