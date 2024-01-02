from random import choice
from time import sleep
import os

from src.views.animation.stop_able_thread import StopAbleThread


class Slot(StopAbleThread):
    def __init__(self):
        super().__init__()
        self.fruits = [
            "🍌",
            "🍒",
            "🍇",
            "🍊",
            "🍓",
            "🍉",
            "🍍",
            "🍐",
            "🍎",
            "🍑",
        ]
        self.screen = [
            [self._get_random_fruit() for _ in range(3)],
            [self._get_random_fruit() for _ in range(3)],
            [self._get_random_fruit() for _ in range(3)],
        ]

    def run(self):
        """Run thread"""
        while not self.is_stopped():
            self._display()
            self._update_screen()
            sleep(0.5)
        if self.is_win:
            fruit_win = self._get_random_fruit()
            self._update_screen([fruit_win, fruit_win, fruit_win])
            self._display()
            sleep(0.5)
            self._update_screen()
            self._display()
        else:
            fruit_1 = self._get_random_fruit()
            self.fruits.remove(fruit_1)
            new_row = [fruit_1, self._get_random_fruit(), self._get_random_fruit()]
            self._update_screen(new_row=new_row)
            self._display()
            sleep(0.5)
            self._update_screen()

    def _update_screen(self, new_row=None):
        """Update screen"""
        if not new_row:
            new_row = [self._get_random_fruit() for _ in range(3)]
        self.screen[2] = self.screen[1]
        self.screen[1] = self.screen[0]
        self.screen[0] = new_row

    def _get_random_fruit(self):
        return choice(self.fruits)

    def _clear_screen(self):
        """Clear screen"""
        if os.name == "nt":
            os.system("cls")
        else:
            os.system("clear")

    def _display(self):
        """Display screen"""
        self._clear_screen()

        print("Machine de la chance")
        print("--------------------------------------------------------")
        print("Pour gagner, il faut avoir 3 fruits identiques sur la ligne du milieu")
        for i in range(3):
            print("".join(self.screen[i]))
