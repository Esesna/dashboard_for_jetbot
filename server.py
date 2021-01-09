import socket


class server:
    def __init__(self, number):
        # ipv4, датаграммный сокет
        self.sock = socket.socket()
        self.sock.bind(('192.168.1.68', 9090))
        self.sock.listen(number)
        self.conn = []
        self.addr = []
        for i in range(number):
            c, a = self.sock.accept()
            self.conn.append(c)
            self.addr.append(a)

    def receive(self, index):
        # формат данных: sysinfo, charge, voltage, x, y
        data = self.conn[index].recv(1024)
        address = self.addr[index]
        return data, address

    def send(self, data, index):
        self.conn[index].send(data)
