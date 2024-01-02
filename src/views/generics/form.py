from abc import ABC, abstractmethod
from consolemenu import ConsoleMenu, PromptUtils
from datetime import datetime
import re


class Form(ABC):
    """A form is a screen that allows the user to enter some data"""

    def __init__(self, parent_menu: ConsoleMenu):
        self.parent_menu = parent_menu

    def _prompt_user(self, message: str, enable_quit: bool = False):
        """Prompt user for input"""
        return (
            PromptUtils(self.parent_menu.screen)
            .input(
                message,
                enable_quit=enable_quit,
                quit_message="(q pour quitter)",
            )
            .input_string
        )

    def _prompt_to_continue(self, message: str | None = None):
        """Prompt user to continue"""
        if message is None:
            message = "Appuyez sur entrée pour continuer."
        else:
            message = f"{message}, appuyez sur entrée pour continuer."

        PromptUtils(self.parent_menu.screen).enter_to_continue(message)

    def _prompt_to_stop_continue(self, message: str):
        """Prompt user to stop or continue"""
        response = ""
        while response not in ["y", "n"]:
            response = self._prompt_user(f"{message} (y/n) : ")
        return response == "y"

    def _prompt_number(
        self, message: str, positive=True, enable_quit: bool = False
    ) -> int:
        """Prompt user for a number"""
        number = self._prompt_user(message, enable_quit=enable_quit)
        try:
            number = int(number)
            if positive and number < 0:
                raise Exception("Number must be positive")
        except Exception:
            print(f"Veuillez entrer un nombre{' positif' if positive else ''}")
            return self._prompt_number(message, enable_quit=enable_quit)
        return number

    def _prompt_date(self, message: str, enable_quit: bool = False) -> datetime:
        """Prompt user for a date"""
        date = self._prompt_user(message + " (jj-mm-aaaa)", enable_quit=enable_quit)
        try:
            date = datetime.strptime(date, "%d-%m-%Y")
        except Exception:
            print("Veuillez entrer une date au format jj-mm-aaaa")
            return self._prompt_date(message, enable_quit=enable_quit)
        return date

    def _prompt_email(self, message: str, enable_quit: bool = False) -> str:
        """Prompt user for an email"""
        email = self._prompt_user(message, enable_quit=enable_quit)
        if re.match(r"^[^@]+@[^@]+\.[^@]+$", email) is None:
            print("Veuillez entrer une adresse email valide")
            return self._prompt_email(message, enable_quit=enable_quit)
        return email

    @abstractmethod
    def execute(self):
        """Execute the form and return the result"""
