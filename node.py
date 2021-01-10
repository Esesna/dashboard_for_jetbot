import socket
import random
import time
import threading

def respond(conn, addr):
    while 1:
        try:
            data = conn.recv(1024)
            s = data.decode()
            
            print('получено ' + s + ' от ' + addr[0])

            if s == 'hello':
                # ToDo: получать данные из топиков 
                charge = random.randint(0, 100)
                voltage = 9 + (charge * 3) // 100
                x = random.randint(0, 49)
                y = random.randint(0, 49)
                response = 'Ubuntu 18.04 LTS, ' + str(charge) + ', ' + str(voltage) + ', ' + str(x) + ', ' + str(y)

                sock.send(response.encode())
                print('ответ: ' + response)

        except ConnectionResetError as e:
            print(e)
            conn.close()
            break
        
def connect(self):
    while 1:
        # ждем подключения
        sock.listen(1)

        # подтверждаем соединение с клиентом
        c, a = sock.accept()

        threading.Thread(target=respond, args=(c,a,), daemon=True).start()

        time.sleep(0.1)

if __name__ == '__main__':
    connections = []

    sock = socket.socket()
    sock.bind(('192.168.1.68'), 9090)

    connector = threading.Thread(target=self.connect, daemon=True)
    connector.start()


    
