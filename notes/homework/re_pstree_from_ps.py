#!/usr/bin/env python
#coding:utf-8

from subprocess import Popen,PIPE
import shlex

def get_ps():
    cmd = 'ps ax -o pid,ppid,cmd'
    subf = Popen(cmd,stdout=PIPE,shell=True)
    return subf.stdout.readlines()[1:]

def data_split():
    data_list = []
    data = get_ps()
    for i in data:
        i_dict = {}
        i_dict['pid'] = shlex.split(i)[0]
        i_dict['ppid'] = shlex.split(i)[1]
        i_dict['cmd'] = ' '.join(shlex.split(i)[2:])
        data_list.append(i_dict)
    return data_list

def show_tree(pid,data_list,deep=2):
    root = [ i for i in data_list if i['pid'] == pid ][0]
    print '-'*deep,root['pid'],root['cmd']
    childs = [i for i in data_list if i['ppid'] == pid]
    if childs:
        deep += 2
        for i in childs:
            show_tree(i['pid'],data_list,deep)

print show_tree('1',data_split())
print get_ps()
