import socket
import random
import time
import threading

def respond(conn, addr):
    state = ["Льзя", 1]
    while 1:
        try:
            data = conn.recv(1024)
            s = data.decode()

            if s == 'hello':
                data = conn.recv(1024)
                s = data.decode()
                # парсим полученную строку
                t = s.split(', ')
                print(state[1])
                tmp = state[1] * int(t[1])
                state = [t[0], tmp]
                # print('получено ' + s + ' от ' + addr[0])

                # if s == 'hello':
                    # ToDo: получать данные из топиков 

                charge = random.randint(0, 100)
                voltage = 9 + (charge * 3) // 100
                x = random.randint(0, 99)
                y = random.randint(0, 99)
                response = 'Ubuntu 18.04 LTS, ' + str(charge) + ', ' + str(voltage) + ', ' + str(x) + ', ' + str(y) + ', ' + str(state[0])

                conn.send(response.encode())
                print('ответ: ' + response + str(state[1]))

        except ConnectionResetError as e:
            print(e)
            conn.close()
            break
        
def connect():
    
    while 1:
        print("ждемс")
        # ждем подключения
        sock.listen(1)

        # подтверждаем соединение с клиентом
        c, a = sock.accept()

        threading.Thread(target=respond, args=(c,a,), daemon=True).start()

        time.sleep(0.1)

if __name__ == '__main__':
    state = []
    connections = []

    sock = socket.socket()
    sock.bind(('192.168.43.4', 9090))
    connect()
    # connector = threading.Thread(target=connect, daemon=True)
    # connector.start()

    
