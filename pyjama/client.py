import socket
from time import sleep

sock = socket.socket(socket.AF_INET,
                     socket.SOCK_DGRAM)

while True:
    sock.sendto(b"Hi!", ('127.0.0.1', 4464))
    sleep(1.0)
