import socket
import random

sock = socket.socket()
sock.connect(('192.168.1.68', 9090))

while 1:
    data = sock.recv(1024)
    if not data:
        continue
    else:
        print('получен ' + data.decode() + ' от сервера')

    charge = random.randint(0, 100)
    voltage = 9 + (charge * 3) // 100
    x = 0
    y = 0
    s = 'Ubuntu 18.04 LTS, ' + str(charge) + ', ' + str(voltage) + ', ' + str(x) + ', ' + str(y) 
    sock.send(s.encode())
