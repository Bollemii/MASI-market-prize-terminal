from abc import ABC, abstractmethod


class IUUIDManager(ABC):
    """Interface for UUIDManager"""

    @abstractmethod
    def generate(self) -> str:
        """Generate a UUID"""

    @abstractmethod
    def is_uuid(self, uuid_string) -> bool:
        """Check if a string is a valid UUID"""
