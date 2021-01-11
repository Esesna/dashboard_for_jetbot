#!/usr/bin/python3
# -*- coding: utf-8 -*-

import sys
import socket
import threading
from PyQt5.QtWidgets import *
from PyQt5.QtGui import *
from PyQt5.QtCore import *
import random
import time
import json


class Map(QWidget):
    #Генерируем карту
    class Robot():
        def __init__(self, x, y):
            #self.id = id
            self.x = x
            self.y = y
    
    def __init__(self):
        self.colSpace =      QColor(220, 220, 220)
        self.colOneRobot =   QColor(167, 200, 100)
        self.colManyRobot =  QColor(0, 150, 255)

        super().__init__()

        #Генерация карты с установленным разрешением countX x countY, больше 50 не советую ставить
        self.countX = 50
        self.countY = 50
        self.mapSizeX,self.mapSizeY = self.readMapSize()
        sizeX = 500
        sizeY = 500
        self.setFixedWidth(sizeX)
        self.setFixedHeight(sizeY)

        self.grd = QGridLayout()
        square = []
        self.rbt = []
        for i in range(30):
            self.rbt.append(self.Robot(-1, -1))

        for i in range(self.countX):
            square.append([])
            for j in range(self.countY):
                square[i].append(QFrame())
                square[i][j].setFixedSize(sizeX/self.countX, sizeY/self.countY)
                # col = QColor(255*i/countX, 255*j/countY, 0)
                col = self.colSpace
                square[i][j].setStyleSheet("QWidget { background-color: %s }" % col.name())
                self.grd.addWidget(square[i][j], i, j)
        
        self.setLayout(self.grd)

    def readMapSize(self):
        with open('tableinf.json', 'r', encoding='utf-8') as f: #открыли файл с данными
            data = json.load(f)
            data = data["Table"]
            # print("x = " + str(data['x']) + "y = " + str(data['y']))
            return data['x'], data['y']

    def updateSquare(self, x, y, col, tooltip):
        point = self.grd.itemAt(int(x * self.countX / self.mapSizeX) + self.countX * int(y * self.countY / self.mapSizeY)).widget()
        point.setToolTip(tooltip)
        point.setStyleSheet("QWidget { background-color: %s }" % col.name())

    def setCrdRobot(self, index, x, y):
        #Обновляем координаты робота на карте        
        if not (self.rbt[index].x == x and self.rbt[index].y == y):
            
            if not (self.rbt[index].x == -1) and not (self.rbt[index].y == -1):
                self.updateSquare(self.rbt[index].x, self.rbt[index].y, self.colSpace, "")

            if not (x == -1) and not (y == -1):
                tooltip = "id = " + str(index+1) + "\nx = " + str(x) + "\ny = " + str(y)
                self.updateSquare(x, y, self.colOneRobot, tooltip)

            self.rbt[index].x = x
            self.rbt[index].y = y

        
class ListRobots(QWidget):
    def __init__(self):
        super().__init__()
        hbox = self.genList(30)
        vbox = QVBoxLayout()
        for tmp in hbox:
            vbox.addLayout(tmp)
        self.setLayout(vbox)

    # генерация списка строк
    def genList(self, amount):
        hbox = []
        for i in range(amount):
            hbox.append(self.genStrRbt(i))
        return hbox

    # интерфейс строки списка ботов
    def genStrRbt(self, i):
        hbox = QHBoxLayout()

        id = QLabel(('0' if (i + 1 < 10) else '') + str(i + 1))
        id.setFixedWidth(20)

        osInf = QLabel("")
        osInf.setFixedWidth(80)

        power = QProgressBar()
        power.setFixedWidth(100)

        U = QLabel(str(20))
        U.setFixedWidth(50)

        motionPermissionButton = QPushButton('Разрешить движение')
        motionPermissionButton.clicked.connect(self.motionPermissionClick)
        motionPermissionButton.setFixedWidth(120)
        motionPermissionButton.index = i
        motionPermissionButton.setEnabled(False)

        emergencyStopButton = QPushButton('Аварийная остановка')
        emergencyStopButton.clicked.connect(self.emergencyStopClick)
        emergencyStopButton.setFixedWidth(120)
        emergencyStopButton.index = i
        emergencyStopButton.setEnabled(False)

        hbox.addWidget(id)                         # 0
        hbox.addWidget(osInf)                      # 1
        hbox.addWidget(power)                      # 2
        hbox.addWidget(U)                          # 3
        hbox.addWidget(motionPermissionButton)     # 4
        hbox.addWidget(emergencyStopButton)        # 5

        return hbox

    def motionPermissionClick(self):
        sender = self.sender()

        if sender.text() == "Разрешить движение":
            sender.setText("Запретить движение")
            sendCommand(sender.index, 'move')
            datatable[sender.index][5] = True
        else:
            sender.setText("Разрешить движение")
            sendCommand(sender.index, 'dont')
            datatable[sender.index][5] = False

    def emergencyStopClick(self):
        sender = self.sender()
        sendCommand(sender.index, 'stop')
        
    def setText(self, column, row, text):
        self.getWidget(column, row).setText(text)

    def setValue(self, column, row, value):
        self.getWidget(column,row).setValue(value)

    def getWidget(self, column, row):
        myLayout = self.layout()
        rowLayout = myLayout.itemAt(row).layout()
        myWidget = rowLayout.itemAt(column).widget()
        return myWidget
        

class Application(QWidget):
    def __init__(self):
        super().__init__()
        self.initUI()

        self._timer = QTimer()
        self._timer.timeout.connect(self.redraw)
        self._timer.start(1000)
            
    def redraw(self):
        for index in range(30):
            data = datatable[index]

            sysinfo = data[0]
            self.lr.setText(1, index, sysinfo)
            capacity = data[1]
            self.lr.setValue(2, index, capacity)
            voltage = ('0' if data[2] < 10 else '') + ("%.2f" % data[2]) + ' В'
            self.lr.setText(3, index, voltage)

            x, y = data[3], data[4]
            self.mp.setCrdRobot(index, x, y)

    def initUI(self):
        self.setGeometry(100, 100, 300, 220)
        self.setWindowTitle('Jetbot Dashboard')
        self.setWindowIcon(QIcon('icon.png'))
        self.show()

        self.lr = ListRobots()

        scroll = QScrollArea()
        scroll.setWidget(self.lr)
        scroll.setFixedWidth(600)
        scroll.move(0, 0)
        scroll.setVerticalScrollBarPolicy(Qt.ScrollBarAlwaysOn)
        scroll.setHorizontalScrollBarPolicy(Qt.ScrollBarAlwaysOff)
        
        # миникарта
        self.mp = Map()
        square = QFrame()
        square.setFixedSize(500, 500)
        self.col = QColor(255, 0, 0)
        square.setStyleSheet("QWidget { background-color: %s }" % self.col.name())

        # настройка расположения элементов
        hbox = QHBoxLayout()
        hbox.addWidget(scroll)
        hbox.addWidget(self.mp)
        # hbox.addWidget(picture)
        self.setLayout(hbox)

        # настройка размеров окна
        self.setMinimumWidth(1200)
        self.setMinimumHeight(550)


def connect(i):
    serverIP = (addr[i], 9090)
    
    while 1:
        time.sleep(1)
        sock = socket.socket()

        try:
            sock.connect(serverIP)
            connections[i] = sock
            ex.lr.getWidget(4, i).setEnabled(True)
            ex.lr.getWidget(5, i).setEnabled(True)
            break

        except TimeoutError as e:
            print(serverIP[0] + ': ' + e.strerror)
            continue

        except OSError as e:
            #print(serverIP[0] + ': ' + e.strerror)
            continue


def disconnect(i):
    # сбрасываем данные
    connections[i].close()
    connections[i] = None
    datatable[i] = ['Not connected', 0, 0, -1, -1, False]
    ex.lr.getWidget(4, i).setEnabled(False)
    ex.lr.setText(4, i, 'Разрешить движение')
    ex.lr.getWidget(5, i).setEnabled(False)

    # пытаемся переподключиться
    threading.Thread(target=connect, args=(i,), daemon=True).start()


def sendCommand(i, com):
    try:
        connections[i].send(com.encode())
    except Exception as e:
        print(addr[i] + ': ' + e.strerror)
        disconnect(i)


def requestData():
    request = 'hello'

    while(1):
        for i in range(30):
            # если робот подключен
            if not (connections[i] == None):
                try:
                    # отправляем команды
                    connections[i].send(request.encode())

                    # получаем ответ
                    data = connections[i].recv(1024)
                    s = data.decode()

                    print(addr[i] + ': ' + s)

                    # парсим полученную строку
                    t = s.split(', ')
                    if len(t) == 5: 
                        sysinfo =   t[0]
                        capacity =    int(t[1])
                        voltage =   float(t[2])
                        x =         float(t[3])
                        y =         float(t[4])

                        # сохраняем данные
                        datatable[i] = [sysinfo, capacity, voltage, x, y, datatable[i][5]]

                except Exception as e:
                    print(addr[i] + ': ' + e.strerror)
                    disconnect(i)
                    continue

        time.sleep(1)

if __name__ == '__main__':
    datatable =     []
    connections =   []
    addr =          []

    with open('listaddress.json', 'r', encoding='utf-8') as f: #открыли файл с данными
        listBot = json.load(f)
        for text in listBot["Bot"]:
            addr.append(text['address'])

    for i in range(30):
        capacity =  0
        voltage =   0
        sysinfo =   'Not connected'
        x =         -1
        y =         -1

        datatable.append([sysinfo, capacity, voltage, x, y, False])

        connections.append(None)
        connectingthread = threading.Thread(target=connect, args=(i,), daemon=True)
        connectingthread.start()

    app = QApplication(sys.argv)
    ex = Application()
    ex.show()

    sendingthread = threading.Thread(target=requestData, daemon=True)
    sendingthread.start()

    sys.exit(app.exec_())
