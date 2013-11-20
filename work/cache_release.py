#!/usr/bin/env python

import sys
from subprocess import Popen,PIPE
import time
import os

class ShellManage():
    name = 'default'
    log = '/var/log/memrelease.log'
    pid_dir = '/var/run/memreleased'
    pid_file = '/var/run/memreleased/memreleased.pid'
    
    def touch_log(self):
        if not os.path.exists(self.log):
            touch_cmd = ['touch', self.log]
            try:
                subf_touch = Popen(touch_cmd, stdout=PIPE, stderr=PIPE)
                err_touch = subf_touch.stderr.read()
            except:
                err_touch = 'The command of touch log could not be done!'
        if not err_touch: print err_touch
        
        chmod_cmd = ['chmod', '666', self.log]
        try:
            subf_chmod = Popen(chmod_cmd, stdout=PIPE, stderr=PIPE)
            err_chmod = subf_chmod.stderr.read()
        except:
            err_chmod = 'The command of chmod log could not be done!'
        if not err_chmod: print err_chmod
    
    def mkdir_pid(self):
        if not os.path.exists(self.pid_dir):
            mk_cmd = ['mkdir', '-p', self.pid_dir]
            try:
                subf_mk = Popen(mk_cmd, stderr=PIPE)
                err_mk = subf_mk.stderr.read()
            except:
                err_mk = 'The command of mkdir pid could not be done!'
        if not err_mk: print err_mk
        
        chmod_cmd = ['chmod', '775', self.pid_dir]
        try:
            subf_chmod = Popen(chmod_cmd, stdout=PIPE, stderr=PIPE)
            err_chmod = subf_chmod.stderr.read()
        except:
            err_chmod = 'The command of chmod 755 %s could not be done!'%self.pid_dir
        if not err_chmod:print err_chmod
    
    def rm_pid_dir(self):
        if os.path.exists(self.pid_dir):
            rm_cmd = ['rm', '-rf', self.pid_dir]
            try:
                subf_rm = Popen(rm_cmd, stdout=PIPE, stderr=PIPE)
                err_rm = subf_rm.stderr.read()
            except:
                err_rm = 'The command of remove the %s could not be done!'%self.pid_dir
        if err_rm:
            self.write_log(err_rm)
    
    def write_log(self,err):
        with open(self.log, 'a') as fp:
            fp.write('\n')
            fp.write(time.strftime('%Y-%m-%d %H:%M:%S',time.localtime(time.time())))
            fp.write('\n')
            fp.write(err)
    
    def start(self):
        ps_cmd = 'ps aux|grep memrelease | grep -v grep | wc -l'
        try:
            subf_ps = Popen(ps_cmd, stdout=PIPE, stderr=PIPE, shell=True)
            err_ps = subf_ps.stderr.read()
            ps_num = int(subf_ps.stdout.read().strip())
        except:
            ps_num = -1
            err_ps = 'Failed! The command of ps for find number of memrelease failed!'
        if err_ps:
            print err_ps
        
        if not os.path.exists(self.pid_file) and ps_num == 0:
            self.mkdir_pid()
            start_cmd = '/usr/local/tnb/memrelease.py'
            subf_start = Popen([start_cmd],stdout=PIPE,stderr=PIPE)
    
    
        
    
    
    

if __name__ == '__main__':
    touch_log()
