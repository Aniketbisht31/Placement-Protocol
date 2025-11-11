import psutil
import time
import threading


class Profiler:
    def __init__(self):
        self.fps = 0
        self.cpu = 0
        self.memory = 0
        self.running = False
        self.thread = None
        self.last_time = time.time()
        self.frame_count = 0

    def start(self):
        self.running = True
        self.thread = threading.Thread(target=self.track, daemon=True)
        self.thread.start()

    def track(self):
        while self.running:
            process = psutil.Process()
            self.cpu = process.cpu_percent(interval=0.5)
            self.memory = process.memory_info().rss / (1024 * 1024)

    def update(self):
        now = time.time()
        self.frame_count += 1
        if now - self.last_time >= 1:
            self.fps = self.frame_count / (now - self.last_time)
            self.frame_count = 0
            self.last_time = now

    def stop(self):
        self.running = False
