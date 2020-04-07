from time import sleep
from argparse import ArgumentParser
from .udp import UDPServer
from .util import daemon, every


class Jammer(UDPServer):
    def __init__(self, serve_ip, serve_port, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.serve_ip = serve_ip
        self.serve_port = serve_port
        self.roster = {}

    def on_message(self, data, ip, port):
        if data['type'] == 'roster':
            self.roster = data['payload']

    def __enter__(self, *args, **kwargs):
        ret = super().__enter__(*args, **kwargs)
        daemon(target=every(0.1, self.say_hello)).start()
        return ret

    def say_hello(self):
        self.sendto({'type': 'greeting', 'name': self.name},
                    (self.serve_ip, self.serve_port))


if __name__ == "__main__":
    parser = ArgumentParser('PyJama client')
    parser.add_argument('ip')
    parser.add_argument('--port', default=4464)
    args = parser.parse_args()

    with Jammer(args.ip, args.port, bind_port=4465) as jam:
        while True:
            print(jam.roster)
            sleep(1)
