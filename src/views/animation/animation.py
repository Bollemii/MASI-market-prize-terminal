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
            [self.get_random_fruit() for _ in range(3)],
            [self.get_random_fruit() for _ in range(3)],
            [self.get_random_fruit() for _ in range(3)],
        ]

    def run(self):
        while not self.is_stopped():
            self.display()
            self.update_screen()
            sleep(0.5)
        if self.is_win:
            fruit_win = self.get_random_fruit()
            self.update_screen([fruit_win, fruit_win, fruit_win])
            self.display()
            sleep(0.5)
            self.update_screen()
            self.display()
        else:
            fruit_1 = self.get_random_fruit()
            self.fruits.remove(fruit_1)
            new_row = [fruit_1, self.get_random_fruit(), self.get_random_fruit()]
            self.update_screen(new_row=new_row)
            self.display()
            sleep(0.5)
            self.update_screen()

    def update_screen(self, new_row=None):
        if not new_row:
            new_row = [self.get_random_fruit() for _ in range(3)]
        self.screen[2] = self.screen[1]
        self.screen[1] = self.screen[0]
        self.screen[0] = new_row

    def get_random_fruit(self):
        return choice(self.fruits)

    def clear(self):
        if os.name == "nt":
            os.system("cls")
        else:
            os.system("clear")

    def display(self):
        self.clear()

        print("Machine de la chance")
        print("--------------------------------------------------------")
        print("Pour gagner, il faut avoir 3 fruits identiques sur la ligne du milieu")
        for i in range(3):
            print("".join(self.screen[i]))
