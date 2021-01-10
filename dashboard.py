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

    def updateSquare(self, x, y, col, tooltip):
        point = self.grd.itemAt(x + self.countX * y).widget()
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
        osInf.setFixedWidth(100)

        power = QProgressBar()
        power.setFixedWidth(100)

        U = QLabel(str(20))

        motionPermissionButton = QPushButton('Разрешить движение')
        motionPermissionButton.clicked.connect(self.motionPermissionClick)
        motionPermissionButton.setFixedWidth(120)
        motionPermissionButton.index = i

        emergencyStopButton = QPushButton('Аварийная остановка')
        emergencyStopButton.clicked.connect(self.emergencyStopClick)
        emergencyStopButton.setFixedWidth(120)
        emergencyStopButton.index = i

        hbox.addWidget(id)                         # 0
        hbox.addWidget(osInf)                      # 1
        hbox.addWidget(power)                      # 2
        hbox.addWidget(U)                          # 3
        hbox.addWidget(motionPermissionButton)     # 4
        hbox.addWidget(emergencyStopButton)        # 5

        return hbox

    def motionPermissionClick(self):
        sender = self.sender()
        print(sender.index)
        if sender.text() == "Разрешить движение":
            sender.setText("Запретить движение")
            statetable[sender.index][0] = "Льзя"
        else:
            sender.setText("Разрешить движение")
            statetable[sender.index][0] = "Незя"
        
        # print(sender.parent().layout().itemAt(1).widget().text())
    def emergencyStopClick(self):
        sender = self.sender()
        statetable[sender.index][1] = 0
        
    def setText(self, column, row, text):
        myLayout = self.layout()
        rowLayout = myLayout.itemAt(row).layout()
        myWidget = rowLayout.itemAt(column).widget()
        myWidget.setText(text)

    def setValue(self, column, row, value):
        myLayout = self.layout()
        rowLayout = myLayout.itemAt(row).layout()
        myWidget = rowLayout.itemAt(column).widget()
        myWidget.setValue(value)
        

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
            charge = data[1]
            self.lr.setValue(2, index, charge)
            voltage = ('0' if data[2] < 10 else '') + str(data[2]) + ' В'
            self.lr.setText(3, index, voltage)

            x, y = data[3], data[4]
            self.mp.setCrdRobot(index, x, y)

            if data[5]=="Льзя":
                self.lr.setText(4, index, "Запретить движение")
            else:
                self.lr.setText(4, index, "Разрешить движение")

    def initUI(self):
        self.setGeometry(100, 100, 300, 220)
        self.setWindowTitle('Jetbot Dashboard')
        self.setWindowIcon(QIcon('icon.png'))
        self.show()

        self.lr = ListRobots()

        scroll = QScrollArea()
        scroll.setWidget(self.lr)
        scroll.setFixedWidth(550)
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
        self.setMinimumWidth(1100)
        self.setMinimumHeight(550)


def connect(i):
    serverIP = (addr[i], 9090)
    
    while 1:
        time.sleep(1)
        sock = socket.socket()

        try:
            sock.connect(serverIP)
            connections[i] = sock
            break

        except TimeoutError as e:
            print(serverIP[0] + ': ' + e.strerror)
            continue

        except OSError as e:
            #print(serverIP[0] + ': ' + e.strerror)
            continue
        

def requestData():
    request = 'hello'

    while(1):
        for i in range(30):
            # если робот подключен
            if not (connections[i] == None):
                try:
                    # отправляем команды
                    connections[i].send(request.encode())

                    data = statetable[i][0] + ', ' + str(statetable[i][1])
                    statetable[i][1] = 1
                    connections[i].send(data.encode())

                    # получаем ответ
                    data = connections[i].recv(1024)
                    s = data.decode()

                    print(addr[i] + ': ' + s)

                    # парсим полученную строку
                    t = s.split(', ')
                    sysinfo =   t[0]
                    charge =    int(t[1])
                    voltage =   int(t[2])
                    x =         int(t[3])
                    y =         int(t[4])
                    mPermis =   t[5]

                    # сохраняем данные
                    datatable[i] = [sysinfo, charge, voltage, x, y, mPermis]
                except ConnectionResetError as e:
                    print(addr[i] + ': ' + e.strerror)
                    
                    # сбрасываем данные
                    connections[i].close()
                    connections[i] = None
                    statetable[i] = ['Not connected', 0, 0, -1, -1]

                    # пытаемся переподключиться
                    threading.Thread(target=connect, args=(i,), daemon=True).start()
                    continue
        time.sleep(1)

if __name__ == '__main__':
    datatable =     []
    connections =   []
    statetable =    []

    addr = ['25.94.21.147',
            '0.0.0.2',
            '0.0.0.3',
            '0.0.0.4',
            '0.0.0.5',
            '0.0.0.6',
            '192.168.43.4',
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

    for i in range(30):
        charge = 0
        voltage = 0
        sysinfo = 'Not connected'
        x = -1
        y = -1
        mPermis = "Льзя"
        datatable.append([sysinfo, charge, voltage, x, y, mPermis])
        connections.append(None)
        statetable.append(["Разрешить движение",1])
        connectingthread = threading.Thread(target=connect, args=(i,), daemon=True)
        connectingthread.start()

    sendingthread = threading.Thread(target=requestData, daemon=True)
    sendingthread.start()

    app = QApplication(sys.argv)
    ex = Application()
    ex.show()
    sys.exit(app.exec_())
