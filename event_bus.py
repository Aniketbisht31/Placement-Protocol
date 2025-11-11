import threading
from collections import deque


class EventBus:
    def __init__(self):
        self.queue = deque()
        self.lock = threading.Lock()

    def post(self, event_type, data):
        with self.lock:
            self.queue.append((event_type, data))

    def get(self):
        with self.lock:
            return self.queue.popleft() if self.queue else None

    def size(self):
        with self.lock:
            return len(self.queue)
