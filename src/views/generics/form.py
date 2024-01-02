from consolemenu import ConsoleMenu, PromptUtils
from datetime import datetime
from abc import ABC, abstractmethod


class Form(ABC):
    """A form is a screen that allows the user to enter some data"""

    def __init__(self, parent_menu: ConsoleMenu):
        self.parent_menu = parent_menu

    def _prompt_user(self, message: str, enable_quit: bool = False):
        return (
            PromptUtils(self.parent_menu.screen)
            .input(
                message,
                enable_quit=enable_quit,
                quit_message="(q pour quitter)",
            )
            .input_string
        )

    def _get_number(self, message: str, positive=True) -> int:
        number = self._prompt_user(message)
        try:
            number = int(number)
            assert number >= 0
        except Exception:
            print("Veuillez entrer un nombre")
            return self._get_number(message)
        return number

    def _get_date(self, message: str) -> datetime:
        date = self._prompt_user(message + " (jj-mm-aaaa)")
        try:
            date = datetime.strptime(date, "%d-%m-%Y")
        except Exception:
            print("Veuillez entrer une date au format jj-mm-aaaa")
            return self._get_date(message)
        return date

    @abstractmethod
    def execute(self):
        """Execute the form and return the result"""
