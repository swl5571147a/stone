#!/usr/bin/env python
#coding:utf-8

import platform
from subprocess import Popen,PIPE
import re_dmidecode
import re_ifconfig
import urllib,urllib2
import json

info = {}

def get_hostname_os():
    info['hostname'] = platform.node()
    info['osver'] = platform.platform()

def get_memory():
    with open('/proc/meminfo') as fp:
        for i in fp.readlines():
            if i.startswith('MemTotal'):
                info['memory'] = int(i.split(':')[1].split()[0].strip())

def get_cpu():
    with open('/proc/cpuinfo') as fp:
        for i in fp.readlines():
            if i.startswith('model name'):
                info['cpu_model'] = i.split(':')[1].strip()
            if i.startswith('cpu cores'):
                info['cpu_num'] = int(i.split(':')[1])

def get_hardware():
    data = re_dmidecode.get_sn(re_dmidecode.get_info(re_dmidecode.get_data()))
    info['product'] = data['Product Name']
    info['vender'] = data['Manufacturer']
    info['sn'] = data['Serial Number']

def get_ipadd():
    data = re_ifconfig.get_info(re_ifconfig.get_data())
    info['ip'] = data['wlan0'][1]

def ret():
    get_hostname_os()
    get_hardware()
    get_cpu()
    get_ipadd()
    get_memory()
    return info

def post(data,des_url):
    data['identity'] = 'sunwenlong'
    #urllib2.urlopen(des_url,urllib.urlencode(data))
    urllib2.urlopen(des_url,json.dumps(data))
    #print urllib.urlencode(data)
    #urllib2.urlopen(des_url,urllib.urlencode(data))
    #print json.dumps(data)

if __name__ == '__main__':
    des_url = 'http://192.168.1.131:8000/api/collect.json'
    #data = json.dumps(ret())
    post(ret(),des_url)
