#!/usr/bin/env python

import os
from subprocess import Popen,PIPE

def get_data():
    cmd = 'ps ax -o pid,ppid,cmd | grep apache2 | grep -v grep'
    data_list = []
    subf = Popen(cmd,stdout=PIPE,shell=True)
    data = subf.stdout.readlines()
    for i in data:
        data_list.append(i.split()[0])
    return data_list

def get_mem():
    cmd = 'free -k'
    subf = Popen(cmd,stdout=PIPE,shell=True)
    data = subf.stdout.readlines()
    mem = data[1].split()[1]
    return mem

def count_rss(data_list):
    join = os.path.join
    sum_rss = 0
    for i in data_list:
        file_path = join(join('/proc',i),'status')
        fp = open(file_path)
        data = fp.readlines()
        for j in data:
            if j.split()[0] == 'VmRSS:':
                sum_rss += int(j.split()[1])
        fp.close()
    return sum_rss

def split_two(s):
    s_p = s.split('.')
    s_n = s_p[1][0:2]
    return '.'.join([s_p[0],s_n])

if __name__ == '__main__':
    a = float(count_rss(get_data()))
    b = float(get_mem())
    print 'Httpd use Mem: %s K'%a
    print 'Httpd share %s%s Mem' %('%',split_two(str(a / b * 100)))
