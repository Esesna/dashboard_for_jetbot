#!/usr/bin/python2
# -*- coding: utf-8 -*-

import socket
import random
import time
import threading
import platform
import rospy
import subprocess
from std_msgs.msg import *
import sys
sys.path.insert(0, '/home/jetbot/jetbot/jetbot')
from ads1115 import *

def respond(conn, addr):
    while 1:
        try:
            data = conn.recv(1024)
            s = data
            
            print('получено ' + s + ' от ' + addr[0])

	    if s == '':
		conn.close()
		break

            if 'hello' in s:
                # заряд и напряжение батареи
                
                voltage = ADS1115().readVoltage(4)/1000.0
                c = (voltage - 7.8)/(12.6-7.8)
		#capacity = (3*c*c-2*c*c*c)*100 # sigmoid?
		capacity = c * 100 # linear

                response = (sysinfo + ', ' +
                            str(capacity) + ', ' +
                            str(voltage) + ', ' +
                            str(x) + ', ' +
                            str(y))

                conn.send(response)
                print('ответ: ' + response)
            
            if 'move' in s:
                motionEnabledFlag = True
		powerOnFlag = True

            if 'dont' in s:
                motionEnabledFlag = False

            if 'stop' in s:
                motionEnabledFlag = False
                powerOnFlag = False

        except Exception as e:
            print(e)
            conn.close()
            break
        
def connect():
    while 1:
        # ждем подключения
        print('Waiting for incoming connection...')
        sock.listen(1)

        # подтверждаем соединение с клиентом
        c, a = sock.accept()

        threading.Thread(target=respond, args=(c,a,)).start()

        time.sleep(0.1)

def callback(data):
    x = data.x_m
    y = data.y_m

def listener():
    rospy.Subscriber(name='hedge_pos_ang', callback=callback)
    rospy.spin()

def talker():
    motionEnabledPublisher = rospy.Publisher(name='motionEnabled', data_class=Bool, queue_size=10)
    powerOnPublisher = rospy.Publisher(name='powerOn', data_class=Bool, queue_size=10)
    rate = rospy.Rate(10)
    while not rospy.is_shutdown():
        motionEnabledPublisher.publish(motionEnabledFlag)
        powerOnPublisher.publish(powerOnFlag)

if __name__ == '__main__':
    connections = []
    sysinfo = platform.platform()

    motionEnabledFlag = False
    powerOnFlag = True

    sock = socket.socket()
    sock.bind(('192.168.2.180', 9090))
    x = 0
    y = 0

    connector = threading.Thread(target=connect)
    connector.start()
    
    rospy.init_node('jb')
    threading.Thread(target=listener).start()

    connector.join()
