import socket
import threading
import time

class server:
    def __init__(self):
        # ipv4, датаграммный сокет
        self.sock = socket.socket()
        self.sock.bind(('192.168.1.68', 9090))

        self.addr = ['0.0.0.1',
                     '0.0.0.2',
                     '0.0.0.3',
                     '0.0.0.4',
                     '0.0.0.5',
                     '0.0.0.6',
                     '192.168.1.72',
                     '0.0.0.8',
                     '0.0.0.9',
                     '0.0.0.10',
                     '0.0.0.11',
                     '0.0.0.12',
                     '0.0.0.13',
                     '0.0.0.14',
                     '0.0.0.15',
                     '0.0.0.16',
                     '0.0.0.17',
                     '0.0.0.18',
                     '0.0.0.19',
                     '0.0.0.20',
                     '0.0.0.21',
                     '0.0.0.22',
                     '0.0.0.23',
                     '0.0.0.24',
                     '0.0.0.25',
                     '0.0.0.26',
                     '0.0.0.27',
                     '0.0.0.28',
                     '0.0.0.29',
                     '0.0.0.30']

        self.conn = [None] * 30

        connector = threading.Thread(target=self.connect, daemon=True)
        connector.start()

    def connect(self):
        while 1:
            # ждем подключения
            self.sock.listen(1)

            # подтверждаем соединение с клиентом
            c, a = self.sock.accept()
            flag = False

            # проверяем адрес подключившегося клиента
            # и по совпадению записываем в массив подключений
            for i in range(len(self.addr)):
                if a[0] == self.addr[i]:
                    self.conn[i] = c
                    flag = True
                    break
        
            # если подключился неизвестный клиент,
            # то закрываем соединение
            if not flag:
                c.close()

            time.sleep(0.1)

    def receive(self, index):
        # формат данных: sysinfo, charge, voltage, x, y
        data = self.conn[index].recv(1024)
        address = self.addr[index]
        return data, address

    def send(self, data, index):
        self.conn[index].send(data)
