from time import sleep
import socketserver
from threading import Thread
import json
import gzip
from contextlib import contextmanager

@contextmanager
def listener(ip, port):
    class InnerServer(socketserver.ThreadingMixIn,
                            socketserver.UDPServer):
        client_list = {}
        
    class UDPHandler(socketserver.BaseRequestHandler):
        def handle(self):
            ip, port = self.client_address
            name = self.request[0].decode()
            InnerServer.client_list[name] = {
                'ip': ip,
                'port': port,
            }
    
    with InnerServer((ip, port), UDPHandler) as server:
        thread = Thread(target=server.serve_forever)
        thread.daemon = True
        thread.start()
        yield server

def notify(sock, client_list):
    message = json.dumps(client_list).encode('utf8')
    message = gzip.compress(message)
    for cli in client_list.values():
        sock.sendto(message, (cli['ip'], cli['port']))

if __name__ == "__main__":
    with listener('0.0.0.0', 4464) as server:
        while True:
            notify(server.socket, server.client_list)
            sleep(0.1)
