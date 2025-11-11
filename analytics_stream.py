import socket
import threading
import json
import time
from datetime import datetime


class AnalyticsServer:
    def __init__(self, ecs, profiler, host='127.0.0.1', port=9090):
        self.ecs = ecs
        self.profiler = profiler
        self.host = host
        self.port = port
        self.clients = []
        self.running = False
        self.server_thread = None
        self.start_time = time.time()

    def start(self):
        self.running = True
        self.server_thread = threading.Thread(target=self.run_server, daemon=True)
        self.server_thread.start()

    def run_server(self):
        sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        sock.bind((self.host, self.port))
        sock.listen(5)
        sock.settimeout(1)
        while self.running:
            try:
                client, _ = sock.accept()
                self.clients.append(client)
            except socket.timeout:
                pass
            self.broadcast()
        sock.close()

    def broadcast(self):
        player = self.ecs.get_player()
        uptime = time.strftime('%H:%M:%S', time.gmtime(time.time() - self.start_time))
        data = {
            "timestamp": datetime.now().isoformat(),
            "uptime": uptime,
            "fps": self.profiler.fps,
            "clients": len(self.clients),
            "players": [
                {"name": player.name, "health": player.health, "score": player.score}
            ] if player else [],
            "events": self.ecs.event_bus.size(),
        }
        msg = json.dumps(data, indent=2).encode()
        for c in list(self.clients):
            try:
                c.sendall(msg + b'\n')
            except:
                self.clients.remove(c)

    def stop(self):
        self.running = False
