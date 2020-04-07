from .udp import UDPServer
from time import sleep

class HolePuncher(UDPServer):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.roster = {}

    def on_message(self, data, ip, port):
        name = data['name']
        self.roster[name] = {
            'ip': ip,
            'port': port
        }

    def notify_all(self):
        for cli in self.roster.values():
            self.sendto({'type': 'roster', 'payload': self.roster},
                        (cli['ip'], cli['port']))


if __name__ == "__main__":
    with HolePuncher('0.0.0.0', 4464) as punch:
        while True:
            punch.notify_all()
            sleep(0.1)
