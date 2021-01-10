import socket
import random
import time
import threading

def response():
    serverIP = ('192.168.1.68', 9090)
    
    while 1:
        sock = socket.socket()
        try:
            sock.connect(serverIP)
        except TimeoutError as e:
            print(e)
            continue

        while 1:
            try:
                data = sock.recv(1024)
            except ConnectionResetError as e:
                print(e)
                sock.close()
                break
            
            if not data:
                continue
            else:
                print('получен ' + data.decode() + ' от сервера')

            charge = random.randint(0, 100)
            voltage = 9 + (charge * 3) // 100
            x = random.randint(0, 49)
            y = random.randint(0, 49)
            s = 'Ubuntu 18.04 LTS, ' + str(charge) + ', ' + str(voltage) + ', ' + str(x) + ', ' + str(y) 
            sock.send(s.encode())
            print('ответ: ' + s)

if __name__ == '__main__':
    threading.Thread(target=response, daemon=True).start()
    
