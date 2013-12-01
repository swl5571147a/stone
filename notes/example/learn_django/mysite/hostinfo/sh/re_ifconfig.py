#!/usr/bin/env python
#coding:utf-8

import re
from subprocess import Popen,PIPE

def get_data():
    subf = Popen(['ifconfig'],stdout=PIPE,stderr=PIPE)
    data = subf.stdout.read()
    source = [i for i in data.split('\n\n') if i.strip() and not i.startswith('lo')]

    return source

def get_info(source):
    info = {}
    r_dev = re.compile(r'^[a-z]+[\d:]{0,3}')
    r_mac = re.compile(r'硬件地址\s([0-9a-f:]{17})',re.I)
    r_ip = re.compile(r'inet 地址:([\d.]{7,15})')
    for i in source:
        dev = r_dev.findall(i)
        mac = r_mac.findall(i,re.M)
        ip = r_ip.findall(i,re.M)
        if ip:
            info[dev[-1]] = [mac[-1],ip[-1]]
        else:
            info[dev[-1]] = [mac[-1],'']
    return info

if __name__ == '__main__':
    print get_info(get_data())
