class TicketNotFoundException(Exception):
    """Ticket not found exception"""

    def __init__(self, message="Ticket not found"):
        self.message = message
        super().__init__(self.message)

    def __str__(self):
        return f"{self.message}"
