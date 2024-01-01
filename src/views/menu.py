from consolemenu import ConsoleMenu, PromptUtils
from consolemenu.items import FunctionItem, SubmenuItem
class Form:
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
        
class Menu(ConsoleMenu):
    def add_form(self, text,form: Form) -> FunctionItem:
        self.append_item(FunctionItem(text, form.execute, menu=self))

    def add_submenu(self, text, submenu: ConsoleMenu):
        seppend_item(SubmenuItem(text, submenu, menu=self))

