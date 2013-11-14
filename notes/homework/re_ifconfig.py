#!/usr/bin/env python
#coding:utf-8

from subprocess import Popen,PIPE

def get_data():
    subf = Popen(['ifconfig'],stdout=PIPE)
    return subf.stdout.read()

def get_info(data):
    data_list = []
    data_line = ''
    for l in [i for i in data.split('\n') if i]:
        if l[0].strip():
            if data_line:
                data_list.append(data_line)
            data_line = l
        else:
            data_line += l
    if data_line:
        data_list.append(data_line)
    return data_list
    
if __name__ == '__main__':
    #print [i for i in get_data().split('\n\n') if not i.startswith('lo')]
    print get_info(get_data())
