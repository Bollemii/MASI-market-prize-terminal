from abc import ABC
from typing import Any, Sequence
from consolemenu import ConsoleMenu
from consolemenu.items import FunctionItem, SubmenuItem

from src.views.generics.form import Form


class Menu(ABC, ConsoleMenu):
    def add_form(self, text: str, form: Form, args: Sequence[Any] | None = None):
        """Add form to menu"""
        self.append_item(FunctionItem(text, form.execute, menu=self, args=args))

    def add_submenu(self, text: str, submenu: "Menu"):
        """Add submenu to menu"""
        self.append_item(SubmenuItem(text, submenu, menu=self))
