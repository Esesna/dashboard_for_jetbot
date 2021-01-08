import socket

class server:
    def __init__(self):
        # ipv4, датаграммный сокет
        self.sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        self.sock.bind(('127.0.0.1', 4141))

    def receive(self):
        # формат данных: sysinfo, charge, voltage, x, y
        data, address = self.sock.recvfrom(1024)
        return data, address

    def send(self, data, address):
        self.sock.sendto(data, address)

