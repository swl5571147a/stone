#!/usr/bin/env python

import socket
import datetime

sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
sock.connect(('127.0.0.1', 2003))

now = datetime.datetime.now()
print 'now:', now
oneday = datetime.timedelta(days=1)
print 'oneday:', oneday
h = now - oneday
print 'h:', h
minutes = datetime.timedelta(minutes=1)
print 'm:', minutes
import random
for i in range(1440):
    h = h + minutes
    s1 = 'test.http_200 %d %s\n' % (random.randint(70, 80), h.strftime('%s'))
    s2 = 'test.http_400 %d %s\n' % (random.randint(80, 90), h.strftime('%s'))
    s3 = 'test.http_500 %d %s\n' % (random.randint(90, 100), h.strftime('%s'))
    sock.send(s1)
    sock.send(s2)
    sock.send(s3)
print h.strftime('%s')