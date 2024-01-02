import signal
import os

from src.application import Application


def _stop_handler(signal, frame):
    """Handle the signal SIGINT"""
    if os.name == "nt":
        os.system("cls")
    else:
        os.system("clear")
    os._exit(0)


if __name__ == "__main__":
    signal.signal(signal.SIGINT, _stop_handler)

    Application().run()
