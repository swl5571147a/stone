#!/usr/bin/env python

from subprocess import Popen, PIPE
import time,os

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
        subf = Popen(release_cmd, stdout=PIPE, stderr=PIPE,shell=True)
        err = subf.stderr.read()
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
    MEM [<%3 Ok] [>3% Warning] [>%10 critical] [>%30 Dangerous]
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
        info['cpu'] = float(data_split[2])
        info['mem'] = float(data_split[3])
        info['rss'] = data_split[5]
        info['start_time'] = data_split[8]
        info['use_time'] = data_split[9]
    else:
        with open('/var/log/memcached.log','a') as fp_data:
            data_log = '\n' + time.strftime('%Y-%m-%d %H:%M:%S',time.localtime(time.time())) + ':' + 'Unknow the service mcu'
            fp_data.write(data_log)
    return info

def restart_service():
    log = '/var/log/memrelease.log'
    current_time_info = time.strftime('%Y-%m-%d %H:%M:%S',time.localtime(time.time()))

    mcu_cmd = ['service','mediamixer','restart']
    try:
        subf_mcu = Popen(mcu_cmd,stdout=PIPE,stderr=PIPE)
        mcu_err = subf_mcu.stderr.read()
    except:
        mcu_err = 'The command of restart mcu could not be done!'
    if mcu_err:
        with open(log,'a') as fp_mcu:
            error_mcu = '\n' + 'Error ' + current_time_info + ':' + mcu_err + info
            fp_mcu.write(error_mcu)
    else:
        with open(log,'a') as fp_mcu:
            ok_mcu = '\n' + 'OK ' + current_time_info + ':' + 'Restart the mcu ok!' + info
            fp_mcu.write(ok_mcu)

    mcuweb_cmd = ['service','mcuWeb','restart']
    try:
        subf_web = Popen(mcuweb_cmd,stderr=PIPE)
        web_err = subf_web.stderr.read()
    except:
        web_err = 'The command of restart mcuWeb could not be done!'
    if web_err:
        with open(log,'a') as fp_web:
            error_web = '\n' + 'Error ' + current_time_info + ':' + web_err + info
            fp_web.write(error_web)
    else:
        with open(log,'a') as fp_web:
            ok_web = '\n' + 'OK ' + current_time_info + ':' + 'Restart the mcuWeb ok!' + info
            fp_web.write(ok_web)

def touch_log():
    log = '/var/log/memcached.log'
    if not os.path.exists(log):
        touch_cmd = ['touch',log]
        try:
            subf_touch = Popen(touch_cmd,stdout=PIPE,stderr=PIPE)
            touch_err = subf_touch.stderr.read()
        except:
            touch_err = 'The command of touch the log could not be done!'
        if touch_err:
            print touch_err

    chmod_cmd = ['chmod','666',log]
    try:
        subf_chmod = Popen(chmod_cmd,stderr=PIPE)
        chmod_err = subf_chmod.stderr.read()
    except:
        chmod_err = 'The command of chmod 666 of the log could not be done!'
    if chmod_err:
        print chmod_err

if __name__ == '__main__':
    log = '/var/log/memrelease.log'
    while True:
        touch_log()
        if float(free_pro()) < 50:
            free_cmd = ['free']
            current_time = time.strftime('%Y-%m-%d %H:%M:%S',time.localtime(time.time()))
            try:
                subf = Popen(free_cmd, stdout=PIPE, stderr=PIPE)
                with open(log, 'a') as fp:
                    fp.write('\n')
                    fp.write(current_time)
                    fp.write('\n')
                    fp.write(subf.stdout.read())
            except:
                with open(log, 'a') as fp:
                    fp.write(current_time)
                    fp.write('\nThe command of free could not be done!\n')
            
            release()
        info = get_mcu_status()
        current_time_info = time.strftime('%Y-%m-%d %H:%M:%S',time.localtime(time.time()))
        if info:
            if 3 < info['mem'] < 10:
                with open(log,'a') as fp_info:
                    warning = '\n' + 'Warning ' + current_time_info + ':' + info
                    fp_info.write(warning)
            elif info['mem'] >= 10 and info['mem'] < 30:
                critical = '\n' + 'Critical ' + current_time_info + ':' + info
                with open(log,'a') as fp_cri:
                    fp_cri.write(critical)
            elif info['mem'] >= 30:
                dangerous = '\n' + 'Dangerous ' + current_time_info + ':' + info
                with open(log,'a') as fp_dan:
                    fp_dan.write(dangerous)
                if not ':' in info['start_time']:
                    restart_service()
                else:
                    use_time = int(info['use_time'].split(':')[0])
                    if use_time > 720:
                        restart_service()
            else:
                pass
        time.sleep(300)
