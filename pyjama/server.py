from .udp import udp_writer, udp_reader
from time import time

class Server:
    def __init__(self):
        self.clients = {}
        self.last_update = None

    def check_and_notify(self, addr):
        ip, port = addr
        if ip not in self.clients:
            self.clients[ip] = port
            self.notify()
        if self.should_update():
            self.notify()

    def notify(self):
        print("notifying!")
        self.last_update = time()

    def should_update(self):
        return len(self.clients) > 0 \
                and self.last_update is not None \
                and time() - self.last_update > 0.1

if __name__ == "__main__":
    server = Server()
    for data, addr in udp_reader():
        print(data, addr)
        server.check_and_notify(addr)
