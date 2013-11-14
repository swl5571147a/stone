#!/usr/bin/env python
#-*- coding:utf-8 -*-

from subprocess import Popen,PIPE

def ReadConfigFile(file_name):
    conf_dict = {}
    with open(file_name) as fp:
        #return [i.strip() for i in fp.readlines() if not i.startswith('#') and i.strip()]
        for i in [i.strip() for i in fp.readlines() if not i.startswith('#') and i.strip()]:
            if len(i.split(' ')) == 1:
                conf_dict[i] = ''
            else:
                conf_dict[i.split(' ')[0]] = i.split(' ')[1]
    return conf_dict

if __name__ == '__main__':
    file_name = '/etc/memcached.conf'
    print ReadConfigFile(file_name)
