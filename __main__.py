from src.views.animation import Slot
import random


if __name__ == "__main__":
    slot = Slot()
    slot.start()
    while True:
        input("Press enter to stop: ")
        break
    win = random.choice([True, False])
    slot.stop(win)
    slot.join()
