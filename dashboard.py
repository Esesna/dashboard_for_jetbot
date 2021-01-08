#!/usr/bin/python3
# -*- coding: utf-8 -*-

import sys
import socket
import threading
from PyQt5.QtWidgets import (QMainWindow, QWidget, QPushButton, QHBoxLayout, QVBoxLayout, QApplication,  QScrollArea, QMessageBox, QLabel, QProgressBar)
from PyQt5.QtGui import QFont, QIcon, QPixmap, QPainter, QColor, QPen
from PyQt5.QtCore import Qt
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
    def genList(self,amount):
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
       
        hbox.addWidget(id)                  #1
        hbox.addWidget(osInf)               #2
        hbox.addWidget(power)               #3
        hbox.addWidget(U)                   #4
        hbox.addWidget(permissionMotion)    #5
        hbox.addWidget(STOP)                #6

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
        
        # potok = threading.Thread(target=self.read_sok)
        # potok.start()
        self.initUI()

    def updateRow(self, index, data):
        ds = data.split(',')
        sysinfo = ds[0]
        self.lr.setText(1, index, sysinfo)
        capacity = int(ds[1])
        self.lr.setValue(2, index, capacity)
        voltage = ('0' if int(ds[2])<10 else '') + ds[2] + ' В'
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

        #qp = QPainter()
        #qp.setPen(Qt.red)
        #for i in range(30):
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

    # def read_sok(self):
    #     while 1 :
    #         data = sor.recv(1024)
    #         print(data.decode('utf-8'))

if __name__ == '__main__':
    # плейсхолдер списка ip
    clients = ['192.168.7.1',
               '192.168.7.2',
               '192.168.7.3',
               '192.168.7.4',
               '192.168.7.5',
               '192.168.7.6',
               '192.168.7.7',
               '192.168.7.8',
               '192.168.7.9',
               '192.168.7.10',
               '192.168.7.11',
               '192.168.7.12',
               '192.168.7.13',
               '192.168.7.14',
               '192.168.7.15',
               '192.168.7.16',
               '192.168.7.17',
               '192.168.7.18',
               '192.168.7.19',
               '192.168.7.20',
               '192.168.7.21',
               '192.168.7.22',
               '192.168.7.23',
               '192.168.7.24',
               '192.168.7.25',
               '192.168.7.26',
               '192.168.7.27',
               '192.168.7.28',
               '192.168.7.29',
               '192.168.7.30']
    # инициализация сервера
    srvr = server()

    app = QApplication(sys.argv)
    ex = Application()

    ###
    # ToDo: вынести обновление в функцию по таймеру
    # ToDo: получать данные с сервера
    # data, address = srvr.recieve()
    # index = clients.index(address)
    # ex.updateRow(index+1, data)
    ###

    # плейсхолдер данных с робота
    for i in range(30):
        capacity = random.randint(0, 100)
        voltage = 9 + (capacity * 3)//100
        data = ('Ubuntu 18.04 LTS' if random.randint(0,1)==0 else 'Windows 10 Pro') + ',' + str(capacity) + ',' + str(voltage)
        ex.updateRow(i+1, data)

    sys.exit(app.exec_())

    
