#!/usr/bin/python3
# -*- coding: utf-8 -*-

import sys
import socket
import threading
from PyQt5.QtWidgets import (QMainWindow, QWidget, QPushButton, QHBoxLayout, QVBoxLayout, QApplication,  QScrollArea, QMessageBox, QLabel, QProgressBar)
from PyQt5.QtGui import QFont, QIcon, QPixmap, QPainter, QColor, QPen
from PyQt5.QtCore import Qt
import random

# class map(QWidget):
#     def 
class ListRobots(QWidget):
    def __init__(self):
        super().__init__()
        hbox = self.genList(30)
        vbox = QVBoxLayout()
        vbox.addStretch(1)
        for tmp in hbox:
            vbox.addLayout(tmp)
        self.setLayout(vbox)

    def genList(self,amount):
        hbox = []
        for i in range(amount):
            hbox.append(self.genStrRbt(i))
            # myWidget = hbox[i].itemAt(2).widget()
        return hbox

    def genStrRbt(self,i):
        hbox = QHBoxLayout()
        hbox.addStretch(1)
 
        id = QLabel(str(i+1))

        osInf = QLabel("Linux")

        power = QProgressBar()

        U = QLabel(str(20))

        permissionMotion = QPushButton('Разрешение движения')
       
        STOP = QPushButton('Аварийная остановка')
       
        hbox.addWidget(id)                  #1
        hbox.addWidget(osInf)               #2
        hbox.addWidget(power)               #3
        hbox.addWidget(U)                   #4
        hbox.addWidget(permissionMotion)    #5
        hbox.addWidget(STOP)                #6

        return hbox

    def setText(self,column,row,text):
        myFirstLayout = self.layout()
        myLayout = myFirstLayout.itemAt(row).layout()
        myWidget = myLayout.itemAt(column).widget()
        myWidget.setText(text)

    def setValue(self,column,row,text):
        myFirstLayout = self.layout()
        myLayout = myFirstLayout.itemAt(row).layout()
        myWidget = myLayout.itemAt(column).widget()
        myWidget.setValue(text)

    # def buttonClicked(self):
    #     sender = self.sender()
    #     Message = QMessageBox.question(self, 'Message',"Are you sure to quit?", QMessageBox.Yes | QMessageBox.No, QMessageBox.No)



class Application(QWidget):
    def __init__(self):
        super().__init__()
        
        # potok = threading.Thread(target= self.read_sok)
        # potok.start()
        self.initUI()

    def initUI(self):

        self.setGeometry(300, 300, 300, 220)
        self.setWindowTitle('Icon')
        self.setWindowIcon(QIcon('web.png'))
        self.show()

        lr = ListRobots()
        
        #Получаем доступ к данным в списке роботов
        

        scroll = QScrollArea()  
        scroll.setWidget(lr)
        scroll.setFixedWidth(500)
        scroll.move(0,0)
        scroll.setVerticalScrollBarPolicy(Qt.ScrollBarAlwaysOn)
        scroll.setHorizontalScrollBarPolicy(Qt.ScrollBarAlwaysOff)
        qp = QPainter()
        qp.setPen(Qt.red)

        for i in range(100):
            x = random.randint(1, 500-1)
            y = random.randint(1, 500-1)
            qp.drawPoint(x, y)

        picture = QLabel(self)
        pixmap = QPixmap('web.png')
        picture.setPixmap(pixmap)

        hbox = QHBoxLayout()
        hbox.addWidget(scroll)
        hbox.addWidget(picture)
        self.setLayout(hbox)

        lr.setValue(3,2,45)

        self.setMinimumWidth(1000)
        self.setMinimumHeight(500)
    # def read_sok(self):
    #     while 1 :
    #         data = sor.recv(1024)
    #         print(data.decode('utf-8'))



if __name__ == '__main__':


    app = QApplication(sys.argv)
    ex = Application()
    sys.exit(app.exec_())