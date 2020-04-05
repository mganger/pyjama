from time import sleep
import socketserver
import json
from threading import Thread
from contextlib import contextmanager
from argparse import ArgumentParser
import uuid

@contextmanager
def register(ip, port):
    class InnerServer(socketserver.ThreadingMixIn, socketserver.UDPServer):
        client_list = None
        name = str(uuid.uuid4())

    class ClientListReceiver(socketserver.BaseRequestHandler):
        def handle(self):
            data = self.request[0].decode()
            InnerServer.client_list = json.loads(data)

    def say_hello(socket):
        while True:
            socket.sendto(InnerServer.name.encode('utf8'),
                          (ip, port))
            sleep(0.1)

    with InnerServer(('0.0.0.0', 4465), ClientListReceiver) as server:
        thread = Thread(target=server.serve_forever)
        thread.daemon = True
        thread.start()

        greeter = Thread(target=say_hello, args=(server.socket,))
        greeter.daemon = True
        greeter.start()

        yield server

if __name__ == "__main__":
    parser = ArgumentParser('PyJama client')
    parser.add_argument('ip')
    parser.add_argument('--port', default=4464)
    args = parser.parse_args()

    with register(args.ip, args.port) as server:
        while True:
            print(server.client_list)
            sleep(1)
