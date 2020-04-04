from .udp import udp_reader, udp_writer
from time import sleep

def message():
    while True:
        yield b"hello"
        sleep(0.5)

if __name__ == "__main__":
    udp_writer(message(), '127.0.0.1', 4464)
