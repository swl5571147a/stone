#!/usr/bin/env python
#-*- coding:utf-8 -*-

from subprocess import Popen,PIPE

def ReadDmidecode():
    subf = Popen(['dmidecode'],stdout=PIPE)
    return subf.stdout.read()

def ReadIfconfig():
    subf = Popen(['ifconfig'],stdout=PIPE)
    return subf.stdout.read()

def SplitData(data):
    data_list = []
    data_line = ''
    for j in [ i for i in data.splitlines() if i]:
        if j[0].strip():
            if data_line:
                data_list.append(data_line)
            data_line = j
        else:
            data_line += ('\n' + j)
    if data_line:
        data_list.append(data_line)
    return data_list

def GetSystemInfo(data):
    return [ i for i in data if i.startswith('System Information')]

def RemoveLoInfo(data):
    return [ i for i in data if not i.startswith('lo')]

def GetDetialInfo(data):
    info_data = [i.strip() for i in data[0].split('\n')][1:]
    return dict(map(lambda x: [i.strip() for i in x.split(':')],info_data))

def GetIpInfo(data):
    ip_data = []
    for i in data:
        dev = i.split('\n')[0].split()[0].strip()
        mac = i.split('\n')[0].split()[-1].strip()
        if i.split('\n')[1].split()[0].strip() == 'inet':
            ip = i.split('\n')[1].split()[1].split(':')[1]
        else:
            ip = ''
        ip_data.append([dev,mac,ip])
    return ip_data

if __name__ == '__main__':
    for key,value in GetDetialInfo(GetSystemInfo(SplitData(ReadDmidecode()))).items():
        if key in ('Manufacturer','Product Name','Serial Number'):
            print '%s:%s'%(key,value)
    print GetIpInfo(RemoveLoInfo(SplitData(ReadIfconfig())))
