from abc import ABC, abstractmethod


class ISingletonDatabase(ABC):
    """Interface for the singleton database class"""

    @abstractmethod
    def get_connection(self):
        """Get the connection"""

    @abstractmethod
    def get_cursor(self):
        """Get the cursor"""
