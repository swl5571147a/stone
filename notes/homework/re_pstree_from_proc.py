#!/usr/bin/env python
#coding:utf-8

from subprocess import Popen,PIPE
import shlex,re,os

def all_num(s):
    if re.match('^[0-9]',s):
        return True

def get_proc():
    data_list = []
    isdir,join = os.path.isdir,os.path.join
    lsdir = os.listdir('/proc')
    dirs = [i for i in lsdir if os.path.isdir(join('/proc',i)) and all_num(i)]
    for i in dirs:
        f = join(join('/proc',i),'status')
        fp = open(f)
        data = fp.readlines()
        for j in data:
            if j.split()[0] == 'Name:':
                cmd = j.split()[1]
            if j.split()[0] == 'PPid:':
                ppid = j.split()[1]
        data_list.append({'pid':i,'ppid':ppid,'cmd':cmd})
    return data_list

def show_tree(pid,data_list,deep=2):
    root = [ i for i in data_list if i['pid'] == pid ][0]
    print '-'*deep,root['pid'],root['cmd']
    childs = [i for i in data_list if i['ppid'] == pid]
    if childs:
        deep += 2
        for i in childs:
            show_tree(i['pid'],data_list,deep)

if __name__ == '__main__':
    print show_tree('1',get_proc())
