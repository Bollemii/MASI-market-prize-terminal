class PasswordException(Exception):
    """Password not valid exception"""

    def __init__(self, message="Password not valid"):
        self.message = message
        super().__init__(self.message)

    def __str__(self):
        return f"{self.message}"
