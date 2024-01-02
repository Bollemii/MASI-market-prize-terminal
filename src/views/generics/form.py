from abc import ABC, abstractmethod
from consolemenu import ConsoleMenu, PromptUtils
from datetime import datetime
import re


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

    def _get_number(
        self, message: str, positive=True, enable_quit: bool = False
    ) -> int:
        number = self._prompt_user(message, enable_quit=enable_quit)
        try:
            number = int(number)
            if positive and number < 0:
                raise Exception("Veuillez entrer un nombre positif")
        except Exception:
            print("Veuillez entrer un nombre")
            return self._get_number(message)
        return number

    def _get_date(self, message: str, enable_quit: bool = False) -> datetime:
        date = self._prompt_user(message + " (jj-mm-aaaa)", enable_quit=enable_quit)
        try:
            date = datetime.strptime(date, "%d-%m-%Y")
        except Exception:
            print("Veuillez entrer une date au format jj-mm-aaaa")
            return self._get_date(message)
        return date

    def _get_email(self, message: str, enable_quit: bool = False) -> str:
        email = self._prompt_user(message, enable_quit=enable_quit)
        if re.match(r"^[^@]+@[^@]+\.[^@]+$", email) is None:
            print("Veuillez entrer une adresse email valide")
            return self._get_email(message)
        return email

    @abstractmethod
    def execute(self):
        """Execute the form and return the result"""
