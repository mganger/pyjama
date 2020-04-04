from .udp import udp_writer, udp_reader
from time import time, sleep

class Server:
    def __init__(self):
        self.clients = {}
        self.next_update = None

    def add(self, addr):
        ip, port = addr
        if ip not in self.clients:
            self.clients[ip] = port
            self.next_update = time()

    def notify(self):
        print("notifying!")
        self.next_update = time() + 0.1

    def should_update(self):
        return len(self.clients) > 0 \
                and self.next_update is not None \
                and time() >= self.next_update

if __name__ == "__main__":
    server = Server()
    with udp_reader() as messages:
        while True:
            if not messages.empty():
                data, addr = messages.get()
                print(data, addr)
                server.add(addr)
            if server.should_update():
                server.notify()
            sleep(0.01)
