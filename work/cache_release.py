#!/usr/bin/env python

import sys
from subprocess import Popen,PIPE
import time
import os

class ShellManage():
    name = 'default'
    log = '/var/log/%s.log' %name
    pid_dir = '/var/run/%s'%name
    pid_file = '/var/run/%s/%s.pid'%(name,name)
    py_script = '/usr/local/tnb/memrelease.py'

    def __init__(self,name,log,pid_dir,pid_file,py_script):
        self.name = name
        self.log = log
        self.pid_dir = pid_dir
        self.pid_file = pid_file
        self.py_script = py_script

    def touch_log(self):
        if not os.path.exists(self.log):
            touch_cmd = ['sudo','touch', self.log]
            try:
                subf_touch = Popen(touch_cmd, stdout=PIPE, stderr=PIPE)
                err_touch = subf_touch.stderr.read()
            except:
                err_touch = 'The command of touch %s.log could not be done!'%self.name
            if err_touch: print err_touch
        
        chmod_cmd = ['sudo','chmod', '666', self.log]
        try:
            subf_chmod = Popen(chmod_cmd, stdout=PIPE, stderr=PIPE)
            err_chmod = subf_chmod.stderr.read()
        except:
            err_chmod = 'The command of chmod log could not be done!'
        if err_chmod:
            print err_chmod
    
    def mkdir_pid(self):
        if not os.path.exists(self.pid_dir):
            mk_cmd = ['sudo','mkdir', '-p', self.pid_dir]
            try:
                subf_mk = Popen(mk_cmd, stderr=PIPE)
                err_mk = subf_mk.stderr.read()
            except:
                err_mk = 'The command of mkdir %s.pid could not be done!'%self.name
            if err_mk: print err_mk
        
        chmod_cmd = ['sudo','chmod', '775', self.pid_dir]
        try:
            subf_chmod = Popen(chmod_cmd, stdout=PIPE, stderr=PIPE)
            err_chmod = subf_chmod.stderr.read()
        except:
            err_chmod = 'The command of chmod 755 %s could not be done!'%self.pid_dir
        if err_chmod:print err_chmod

        touch_cmd = ['sudo','touch',self.pid_file]
        ch_touch_cmd = ['sudo','chmod','755',self.pid_file]
        try:
            if not os.path.exists(self.pid_file):
                subf_touch = Popen(touch_cmd)
            subf_ch = Popen(ch_touch_cmd)
        except:
            print 'error'
    
    def rm_pid_dir(self):
        if os.path.exists(self.pid_dir):
            rm_cmd = ['sudo','rm', '-rf', self.pid_dir]
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
        ps_cmd = 'ps aux|grep %s | grep -v grep | wc -l'%self.name
        try:
            subf_ps = Popen(ps_cmd, stdout=PIPE, stderr=PIPE, shell=True)
            err_ps = subf_ps.stderr.read()
            ps_num = int(subf_ps.stdout.read().strip())
        except:
            ps_num = -1
            err_ps = 'Failed! The command of ps for find number of %s failed!'%self.name
        if err_ps:
            print err_ps
        
        if ps_num == 0:
            try:
                subf_start = Popen([self.py_script])
                err_start = ''
                pid = str(subf_start.pid)
            except:
                err_start = 'The command of start the py_script colud not be done!'
            if not err_start:
                self.touch_log()
                self.mkdir_pid()
                with open(self.pid_file,'w') as fp_pid:
                    fp_pid.write(pid)
                with open(self.log,'a') as fp_log:
                    start_log = time.strftime('%Y-%m-%d %H:%M:%S',time.localtime(time.time())) + ':' + 'Sucessfully start!' + '\n'
                    fp_log.write(start_log)
                print 'Done! The %s is running now, the pid is %s' %(self.name,pid)
            else:
                print err_start
        else:
            print 'Waring!The %s is running, Could not be start. You can use restart or stop to test!'%self.name

    def stop(self):
        try:
            with open(self.pid_file) as fp:
                pid = fp.read().strip()
        except:
            pid = self.get_pid()
            print 'Warning! The pid file is not exists!'
        if pid:
            stop_cmd = ['sudo','kill','-15',pid]
            try:
                subf_stop = Popen(stop_cmd,stderr=PIPE)
                err_stop = subf_stop.stderr.read()
            except:
                err_stop = 'The command of stop the %s could not be done!'%self.name
            if err_stop:
                print err_stop
            else:
                print 'Done! The command of stop the %s is done!' %self.name
                stop_log = time.strftime('%Y-%m-%d %H:%M:%S',time.localtime(time.time())) + ':' + 'Sucessfully stop!' + '\n'
                with open(self.log,'a') as fp_log:
                    fp_log.write(stop_log)
        else:
            print 'Error! The %s is not running!' %self.name

        self.rm_pid_dir()

    def status(self):
        grep_pid = self.get_pid()
        if grep_pid:
            try:
                with open(self.pid_file) as fp:
                    file_pid = fp.read().strip()
            except:
                file_pid = ''
            if grep_pid == file_pid:
                print 'The %s is running : %s'%(self.name,grep_pid)
            else:
                print 'Warning!The %s is running: %s, but it seem work in bad status.' %(self.name,grep_pid)
        else:
            print 'The %s is not running'%self.name

    def restart(self):
        pid = self.get_pid()
        if pid:
            self.stop()
            self.start()
        else:
            print 'Warning! Nothing to be done, because the %s is not running!'%self.name
            self.start()

    def get_pid(self):
        grep_cmd = 'ps aux|grep %s|grep -v grep'%self.name
        try:
            subf_grep = Popen(grep_cmd,stdout=PIPE,stderr=PIPE,shell=True)
            data_grep = subf_grep.stdout.read()
            err_grep = subf_grep.stderr.read()
        except:
            err_grep = 'The command of grep %s could not be done!'%self.name
            data_grep = ''
        if err_grep:
            print err_grep
        if data_grep:
            grep_pid = data_grep.split()[1]
        else:
            grep_pid = ''
        return grep_pid
    
if __name__ == '__main__':
    name='memrelease'
    log = '/var/log/%s.log' %name
    pid_dir = '/var/run/%s'%name
    pid_file = '/var/run/%s/%s.pid'%(name,name)
    py_script = './memrelease.py'
    sm = ShellManage(name=name,log=log,pid_dir=pid_dir,pid_file=pid_file,py_script=py_script)
    try:
        if sys.argv[1] == 'start':
            sm.start()
        elif sys.argv[1] == 'stop':
            sm.stop()
        elif sys.argv[1] == 'status':
            sm.status()
        elif sys.argv[1] == 'restart':
            sm.restart()
        else:
            print 'Only {start|stop|status|restart} can be used!'
    except:
        print 'You should use {start|stop|status|restart} to use it!'
    

