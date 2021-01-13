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
import psutil

def respond(conn, addr):
    while 1:
        try:
            data = conn.recv(1024)
            s = data
            
            print('получено ' + s + ' от ' + addr[0])

            if 'hello' in s:
                # заряд и напряжение батареи
                '''
                bashCommand = "cat /sys/class/power_supply/BAT0/uevent"
                process = subprocess.Popen(bashCommand.split(), stdout=subprocess.PIPE)
                output, error = process.communicate()
                voltage = 0
                capacity = 0
                lines = output.split('\n')
                for line in lines:
                    if "POWER_SUPPLY_VOLTAGE_NOW=" in line:
                        voltage = int(line.split('=')[1]) / float(1000000)
                    elif "POWER_SUPPLY_CAPACITY=" in line:
                        capacity = int(line.split('=')[1])
                        '''
                
                voltage = psutil.sensors_battery()[0]
                capacity = 0

                response = (sysinfo + ', ' +
                            str(capacity) + ', ' +
                            str(voltage) + ', ' +
                            str(x) + ', ' +
                            str(y))

                conn.send(response)
                print('ответ: ' + response)
            
            if 'move' in s:
                motionEnabledFlag = True

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
