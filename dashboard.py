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


class ListRobots(QWidget):
    def __init__(self):
        super().__init__()
        hbox = self.genList(30)
        vbox = QVBoxLayout()
        vbox.addStretch(1)
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
        id.move(0, 0)

        osInf = QLabel("")
        osInf.setFixedWidth(100)
        osInf.move(id.width() + 10, 0)

        power = QProgressBar()
        power.setFixedWidth(100)
        power.move(id.width() + osInf.width() + 20, 0)

        U = QLabel(str(20))

        permissionMotion = QPushButton('Разрешить движение')
        permissionMotion.setFixedWidth(120)

        STOP = QPushButton('Аварийная остановка')
        STOP.setFixedWidth(120)

        hbox.addWidget(id)                  # 0
        hbox.addWidget(osInf)               # 1
        hbox.addWidget(power)               # 2
        hbox.addWidget(U)                   # 3
        hbox.addWidget(permissionMotion)    # 4
        hbox.addWidget(STOP)                # 5

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

    # def buttonClicked(self):
    #     sender = self.sender()
    #     Message = QMessageBox.question(self, 'Message',"Are you sure to quit?", QMessageBox.Yes | QMessageBox.No, QMessageBox.No)

class Application(QWidget):
    def __init__(self):
        super().__init__()
        self.initUI()

        self._timer = QTimer()
        self._timer.timeout.connect(self.update_rows)
        self._timer.start(1000)

    def update_rows(self):
        for i in range(30):
            data = datatable[i]
            index = i + 1
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

        # qp = QPainter()
        # qp.setPen(Qt.red)
        # for i in range(30):
        #    x = random.randint(1, 500-1)
        #    y = random.randint(1, 500-1)
        #    qp.drawPoint(x, y)

        # плейсхолдер миникарты
        picture = QLabel(self)
        pixmap = QPixmap('icon.png')
        picture.setPixmap(pixmap)

        # настройка расположения элементов
        hbox = QHBoxLayout()
        hbox.addWidget(scroll)
        hbox.addWidget(picture)
        self.setLayout(hbox)

        # настройка размеров окна
        self.setMinimumWidth(1400)
        self.setMinimumHeight(910)


def sender():
    srvr = server(numofclients)

    while(1):
        for i in range(numofclients):
            s = 'запрос'
            srvr.send(s.encode(), i)
            data, address = srvr.receive(i)
            s = data.decode()
            t = s.split(', ')
            sysinfo = t[0]
            charge = int(t[1])
            voltage = int(t[2])
            x = int(t[3])
            y = int(t[4])
            datatable[i] = [sysinfo, charge, voltage, x, y]
        time.sleep(1)


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

    app = QApplication(sys.argv)
    ex = Application()
    ex.show()
    sys.exit(app.exec_())
