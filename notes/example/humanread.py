#!/usr/bin/env python

def ret(data):
    ret_data = ''
    if data < 1024:
        ret_data = str(data) + 'B'
    elif 1024 < data < 1048576:
        data /= 1024.0
        ret_data = str(data) + 'K'
    elif 1048576 < data < 1073741824:
        data /= (1024*1024.0)
        ret_data = str(data) + 'M'
    elif 1073741824 < data < 1099511627776:
        data /= (1024*1024*1024.0)
        ret_data = str(data) + 'G'

    return ret_data

unit = [('b',1),('k',1024),('m',1024*1024),('g',1024*1024*1024),('t',1024*1024*1024*1024)]
def conver2unit(v):
    for k,j in unit:
        n = v/j
        if n < 1024:
            return n,k
    return n,k

print ret(11111)