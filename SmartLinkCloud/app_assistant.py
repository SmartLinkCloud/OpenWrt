#!/usr/bin/python

import socket
import time

def tcplink(sock, addr):
    print 'Accept new connection from %s:%s...' % addr
    sock.send('Welcome!')
    while True:
        data = sock.recv(1024)
        time.sleep(1)
        if data == 'exit' or not data:
            break
        sock.send('Hello, %s!' % data)
    sock.close()
    print 'Connection from %s:%s closed.' % addr
##----------------------------------------------------------------------##

def app_assistant():
    '''app_assistant communicate with gateway'''
    print "ok"


##----------------------------------------------------------------------##

if __name__ == '__main__':

    dbname = 'SmartLinkCloud.db'

    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    #s.bind(('192.168.5.1', 6080))
    s.bind(('127.0.0.1', 6080))
    s.listen(5)
    print 'Waiting for connection...'

    while True:
        sock, addr = s.accept()
        t = threading.Thread(target=tcplink, args=(sock, addr))
        t.start()

