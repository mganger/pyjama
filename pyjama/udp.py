import socket
from time import sleep
from queue import Queue
from threading import Thread
from contextlib import contextmanager
import gzip
import json
from .util import daemon
import uuid
import socketserver

def encode_msg(data):
    data = json.dumps(data)
    data = data.encode('utf8')
    data = gzip.compress(data)
    return data

def decode_msg(data):
    data = gzip.decompress(data)
    data = data.decode()
    data = json.loads(data)
    return data

class UDPServer:
    def __init__(self, bind_ip=None, bind_port=None):
        self.bind_ip = bind_ip or '0.0.0.0'
        self.bind_port = bind_port or 4464
        self.name = str(uuid.uuid4())

        class InnerServer(socketserver.ThreadingMixIn, socketserver.UDPServer):
            pass

        class ClientListReceiver(socketserver.BaseRequestHandler):
            def handle(inner_self):
                self._handle_raw(inner_self)

        self.server = InnerServer((self.bind_ip, self.bind_port),
                                  ClientListReceiver)
        self.socket = self.server.socket

    def __enter__(self):
        self.server.__enter__()
        daemon(target=self.server.serve_forever).start()
        return self

    def __exit__(self, *args, **kwargs):
        self.server.__exit__(*args, **kwargs)

    def _handle_raw(self, req):
        data = req.request[0]
        data = decode_msg(data)
        ip, port = req.client_address
        self.on_message(data, ip=ip, port=port)

    def sendto(self, message, *args, **kwargs):
        message = encode_msg(message)
        return self.socket.sendto(message, *args, **kwargs)

    def on_message(self, *args, **kwargs):
        raise NotImplementedError()
        

@contextmanager
def udp_reader(ip=None, port=4464, buf=1024):
    ip = ip or '0.0.0.0'
    sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    sock.bind((ip, port))
    q = Queue()
    def _inner():
        while True:
            q.put(sock.recvfrom(buf))
    thread = Thread(target=_inner)
    thread.start()
    yield q

def udp_writer(data, ip, port=4464):
    sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    for x in data:
        sock.sendto(x, (ip, port))
