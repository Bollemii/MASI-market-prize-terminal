from consolemenu import ConsoleMenu
from consolemenu.items import FunctionItem, SubmenuItem

from src.views.generics.form import Form


class Menu(ConsoleMenu):
    def add_form(self, text, form: Form):
        """Add form to menu"""
        self.append_item(FunctionItem(text, form.execute, menu=self))

    def add_submenu(self, text, submenu: ConsoleMenu):
        """Add submenu to menu"""
        self.append_item(SubmenuItem(text, submenu, menu=self))
