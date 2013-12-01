#/usr/bin/env python

import paramiko
import time
import threading

def get_data(ip,username,passwd):
    ssh = paramiko.SSHClient()
    ssh.load_system_host_keys()
    ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
    ssh.connect(hostname=ip,username=username,password=passwd)
    stdin,stdout,stderr = ssh.exec_command('date')

    print stdout.read(),'\t%s' %ip
    ssh.close()

def main():
    a = threading.Thread(target=get_data,args=('192.168.1.113','stone','stone'))
    b = threading.Thread(target=get_data,args=('192.168.1.128','stone','stone'))
    a.start()
    time.sleep(0.5)
    b.start()
    time.sleep(0.5)
    a.join()
    b.join()
    time.sleep(0.5)
    print 'End......'

if __name__ == '__main__':
    main()