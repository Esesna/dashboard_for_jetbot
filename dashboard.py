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

    def update_square(self, x, y, col, tooltip):
        point = self.grd.itemAt(x + self.countX * y).widget()
        point.setToolTip(tooltip)
        point.setStyleSheet("QWidget { background-color: %s }" % col.name())

    def setCrdRobot(self, index, x, y):
        #Обновляем координаты робота на карте        
        if not (self.rbt[index].x == x and self.rbt[index].y == y):
            
            if not (self.rbt[index].x == -1) and not (self.rbt[index].y == -1):
                self.update_square(self.rbt[index].x, self.rbt[index].y, self.colSpace, "")

            if not (x == -1) and not (y == -1):
                tooltip = "id = " + str(index+1) + "\nx = " + str(x) + "\ny = " + str(y)
                self.update_square(x, y, self.colOneRobot, tooltip)

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
    srvr = server()
    request = 'дай манки'

    while(1):
        for i in range(30):
            # если робот подключен
            if not (srvr.conn[i] == None):
                try:
                    # отправляем запрос
                    srvr.send(request.encode(), i)

                    # получаем ответ
                    data, address = srvr.receive(i)
                    s = data.decode()

                    print('получено: ' + s)

                    # парсим полученную строку
                    t = s.split(', ')
                    sysinfo = t[0]
                    charge = int(t[1])
                    voltage = int(t[2])
                    x = int(t[3])
                    y = int(t[4])

                    # сохраняем данные
                    datatable[i] = [sysinfo, charge, voltage, x, y]
                except ConnectionResetError as e:
                    print(e)
                    srvr.conn[i] = None
                    datatable[i] = ['Not connected', 0, 0, -1, -1]
                    continue
        time.sleep(1)

if __name__ == '__main__':
    datatable = []
    # плейсхолдер данных с робота
    for i in range(30):
        charge = 0
        voltage = 0
        sysinfo = 'Not connected'
        x = -1
        y = -1
        datatable.append([sysinfo, charge, voltage, x, y])

    sendingthread = threading.Thread(target=sender, daemon=True)
    sendingthread.start()

    app = QApplication(sys.argv)
    ex = Application()
    ex.show()
    sys.exit(app.exec_())
