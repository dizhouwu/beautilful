import threading
import pandas as pd

class LockedIterator:
    def __init__(self, it):
        self._lock = threading.Lock()
        self._it = it.__iter__()

    def __iter__(self):
        return self

    def __next__(self):
        with self._lock:
            return next(self._it)
