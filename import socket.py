import socket
import threading


sock = socket.socket (socket.AF_INET, socket.SOCK_DGRAM)
sock.bind (('',5050))