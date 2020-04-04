import socket
from time import sleep

def udp_reader(ip=None, port=4464, buf=1024):
    ip = ip or '0.0.0.0'
    sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    sock.bind((ip, port))
    while True:
        yield sock.recvfrom(buf)

def udp_writer(data, ip, port=4464):
    sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    for x in data:
        sock.sendto(x, (ip, port))
