from src.views.animation import Slot


if __name__ == "__main__":
    slot = Slot()
    slot.start()
    while True:
        input("Press enter to stop: ")
        break
    slot.stop(is_win=False)
    slot.join()
