#!/usr/bin/env python
#-*- coding:utf-8 -*-

from subprocess import Popen,PIPE

def get_data():
    subf = Popen(['sudo','dmidecode'],stdout=PIPE)
    return subf.stdout.read()

def get_info(data):
    data_list = []
    data_line = ''
    for j in [i for i in data.split('\n') if i]:
        if j[0].strip():
            if data_line:
                data_list.append(data_line)
            data_line = (j + '\n')
        else:
            data_line += (j + '\n')
    if data_line:
        data_list.append(data_line)
    for i in data_list:
        if i.startswith('System Information'):
            return i

def get_sn(s):
    d = [i.strip() for i in s.splitlines()][1:]
    return dict(map(lambda x: [i.strip() for i in x.split(':')],d))

if __name__ == '__main__':
    print get_sn(get_info(get_data()))
