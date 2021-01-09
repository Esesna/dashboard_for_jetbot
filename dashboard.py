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
from server import *

class Map(QWidget):
    #Генерируем карту
    class Robot():
        def __init__(self,id,x,y):
            self.id = id
            self.x = x
            self.y = y
        
    def __init__(self):
        self.colSpace =      QColor(220, 220, 220)
        self.colOneRobot =   QColor(0, 0, 255)
        self.colManyRobot =  QColor(0, 150, 255)
        super().__init__()
        #Генерация карты с установленным разрешением countX x countY, больеш 50 не советую ставить
        self.countX = 50
        self.countY = 50
        sizeX = 500
        sizeY = 500
        self.setFixedWidth(sizeX)
        self.setFixedHeight(sizeY)
        self.grd = QGridLayout()
        square = []
        self.rbt = [] 
        for i in range(0, self.countX):
            square.append([])
            for j in range(0, self.countY):
                square[i].append(QFrame())
                square[i][j].setFixedSize(sizeX/self.countX, sizeY/self.countY)
                # col = QColor(255*i/countX, 255*j/countY, 0)
                col = self.colSpace
                square[i][j].setStyleSheet("QWidget { background-color: %s }" % col.name())
                self.grd.addWidget(square[i][j], i, j)
        
        self.setLayout(self.grd)

    def addRobot(self,index,x,y):
        #Если робота нет в списке, инициализирует
        self.rbt.append(self.Robot(index,x,y))

        myLayout = self.layout()
        point = self.grd.itemAt(x+self.countX*y).widget()
        col = self.colOneRobot
        point.setToolTip("id = " + str(index) + "\nx = " + str(x) + "\ny = " + str(y))
        point.setStyleSheet("QWidget { background-color: %s }" % col.name())
        self.rbt[index].x = x
        self.rbt[index].y = y

    def setCrdRobot(self,index,x,y):
        #Обновляем координаты робота на карте        
        if index < len(self.rbt):

            if not(self.rbt[index].x == x and self.rbt[index].y == y):
                myLayout = self.layout()

                point = self.grd.itemAt(self.rbt[index].x + self.countX * self.rbt[index].y).widget()
                col = self.colSpace
                point.setToolTip("")
                point.setStyleSheet("QWidget { background-color: %s }" % col.name())

                point = self.grd.itemAt(x + self.countX * y).widget()
                col = self.colOneRobot
                point.setToolTip("id = " + str(index) + "\nx = " + str(x) + "\ny = " + str(y))
                point.setStyleSheet("QWidget { background-color: %s }" % col.name())

                self.rbt[index].x = x
                self.rbt[index].y = y
        else:
            self.addRobot(index,x,y)



        
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
        motionPermissionButton.setFixedWidth(120)

        emergencyStopButton = QPushButton('Аварийная остановка')
        emergencyStopButton.setFixedWidth(120)

        hbox.addWidget(id)                         # 0
        hbox.addWidget(osInf)                      # 1
        hbox.addWidget(power)                      # 2
        hbox.addWidget(U)                          # 3
        hbox.addWidget(motionPermissionButton)     # 4
        hbox.addWidget(emergencyStopButton)        # 5

        return hbox

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
        self._timer.timeout.connect(self.update_data)
        self._timer.start(1000)

    def update_data(self):
        self.update_map()
        self.update_rows()

    def update_map(self):
        for index in range(30):
            data = datatable[index]
            self.mp.setCrdRobot(index,data[3],data[4])

    def update_rows(self):
        for index in range(30):
            data = datatable[index]
            sysinfo = data[0]
            self.lr.setText(1, index, sysinfo)
            charge = data[1]
            self.lr.setValue(2, index, charge)
            voltage = ('0' if data[2] < 10 else '') + str(data[2]) + ' В'
            self.lr.setText(3, index, voltage)

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

        # плейсхолдер миникарты
        picture = QLabel(self)
        pixmap = QPixmap('icon.png')
        picture.setPixmap(pixmap)
        Label = QLabel("Какашка")
        
        #test
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


def sender():
    srvr = server(numofclients)

    while(1):
        for i in range(numofclients):
            s = 'дай манки'
            srvr.send(s.encode(), i)
            data, address = srvr.receive(i)
            s = data.decode()
            print('получено: ' + s)
            t = s.split(', ')
            sysinfo = t[0]
            charge = int(t[1])
            voltage = int(t[2])
            x = int(t[3])
            y = int(t[4])
            datatable[i] = [sysinfo, charge, voltage, x, y]

        time.sleep(1)

def node():
    sock = socket.socket()
    sock.connect(('25.94.21.147', 9090))

    while 1:
        data = sock.recv(1024)
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

if __name__ == '__main__':
    datatable = []
    # плейсхолдер данных с робота
    for i in range(30):
        charge = 0
        voltage = 0
        sysinfo = 'Not connected'
        x = 0
        y = 0
        datatable.append([sysinfo, charge, voltage, x, y])

    numofclients = 1
    sendingthread = threading.Thread(target=sender, daemon=True)
    sendingthread.start()

    nodethread = threading.Thread(target=node, daemon=True)
    nodethread.start()

    app = QApplication(sys.argv)
    ex = Application()
    ex.show()
    sys.exit(app.exec_())
