import socket
from time import sleep
from queue import Queue
from threading import Thread
from contextlib import contextmanager

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
