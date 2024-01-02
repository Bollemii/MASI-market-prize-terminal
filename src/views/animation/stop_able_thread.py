from threading import Thread, Event


class StopAbleThread(Thread):
    def __init__(self):
        super().__init__()
        self._stop_event = Event()

    def stop(self, is_win=False):
        """Stop thread"""
        self.is_win = is_win
        self._stop_event.set()

    def is_stopped(self):
        """Check if thread is stopped"""
        return self._stop_event.is_set()
