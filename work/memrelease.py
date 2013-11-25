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

def get_mcu_status():
    '''CPU [>%150 Warning] [>%300 Dangerous]
    MEM [>%10 Warning] [>%30 Dangerous]
    time [>1440 restart] [<1440 count]
    count [30s * 20 restart]
    '''
    info =  {}
    cmd = 'ps aux|grep mcu|grep -v grep'
    try:
        subf = Popen(cmd,stdout=PIPE,stderr=PIPE,shell=True)
        data = subf.stdout.readlines()
        cmd_err = subf.stderr.read()
    except:
        cmd_err = 'Error! The command of grep mcu could not be done!'
        data = ''
    if cmd_err:
        with open('/var/log/memcached.log','a') as fp:
            err_data = '\n' + time.strftime('%Y-%m-%d %H:%M:%S',time.localtime(time.time())) + ':' + cmd_err
            fp.write(err_data)
    if data:
        data_split = data[1].split()
        info['pid'] = data_split[1]
        info['cpu'] = data_split[2]
        info['mem'] = data_split[3]
        info['rss'] = data_split[5]
        info['time']
    else:
        with open('var/log/memcached.log','a') as fp_data:
            data_log = '\n' + time.strftime('%Y-%m-%d %H:%M:%S',time.localtime(time.time())) + ':' + 'Unknow the service mcu'
            fp_data.write(data_log)


if __name__ == '__main__':
    while True:
        if float(free_pro()) > 50:
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
    
