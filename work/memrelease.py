#!/usr/bin/env python

from subprocess import Popen, PIPE
import time

def free_pro():
    with open('/proc/meminfo') as fp:
        for i in fp.readlines():
            if i.startswith('MemFree'):
                MemFree = float(i.split()[1])
            if i.startswith('MemTotal'):
                MemTotal = float(i.split()[1])
    
    return '%.2f'%(MemFree / MemTotal * 100)
 
def release():
    sync = ['sync']
    release_cmd = 'echo 3 > /proc/sys/vm/drop_caches'
    try:
        Popen(sync, stdout=PIPE, stderr=PIPE)
        Popen(sync, stdout=PIPE, stderr=PIPE)
        Popen(release_cmd, stdout=PIPE, stderr=PIPE, shell=True)
    except:
        err = 'The cmd release could not be done!'
    if err:
        with open('/var/log/memrelease.log', 'a') as fp:
            fp.write('\n')
            fp.write(time.strftime('%Y-%m-%d %H:%M:%S',time.localtime(time.time())))
            fp.write('\n')
            fp.write(err)

if __name__ == '__main__':
    while True:
        if float(free_pro()) > 70:
            free_cmd = ['free']
            current_time = time.strftime('%Y-%m-%d %H:%M:%S',time.localtime(time.time()))
            try:
                subf = Popen(free_cmd, stdout=PIPE, stderr=PIPE)
                with open('/var/log/memrelease.log', 'a') as fp:
                    fp.write('\n')
                    fp.write(current_time)
                    fp.write('\n')
                    fp.write(subf.stdout.read())
            except:
                with open('/var/log/memrelease.log', 'a') as fp:
                    fp.write(current_time)
                    fp.write('\nThe command of free could not be done!\n')
            
            release()
    
