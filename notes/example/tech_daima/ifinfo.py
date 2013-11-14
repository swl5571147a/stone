#!/usr/bin/env python

from subprocess import Popen, PIPE
import pprint

def readIfconfig():
    p = Popen(['ifconfig'],stdout=PIPE)
    return p.stdout.read()

def readDmidecode():
    p = Popen(['dmidecode'], stdout = PIPE )
    return p.communicate()[0]

def splitData(data):
    ret = []
    d = ""
    for l in [i for i in data.split('\n') if i]:
        if l[0].strip():
            if d:
                ret.append(d)
            d = l
        else:
            d +='\n'+l
    if d: ret.append(d)
    return ret 

def parseIfcfg(data):
    lines = data.split('\n')
    ifname = lines[0].split()[0]
    macaddr = lines[0].split()[-1]
    ipaddr = lines[1].split()[1].split(':')[1]
    return ifname, macaddr, ipaddr

def parseDmidecode(data):
    d = [i.strip() for i in data.splitlines()][1:]
    #return dict([i.split(':') for i in d])
    #return dict(map(lambda x: [i.strip() for i in x.split(':')], d))
    return dict([[j.strip() for j in i.split(':')] for i in d])

if __name__ == '__main__':
    #for i in [i for i in [i.strip() for i in readIfconfig().split('\n\n') if not i.startswith('lo')] if i]:
    #for i in splitData(readIfconfig()):
    #    print parseIfcfg(i)
    for i in splitData(readDmidecode()):
        if i.startswith('System'):
            pprint.pprint(parseDmidecode(i))
