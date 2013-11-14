#!/usr/bin/env python

import sys, os
from subprocess import Popen, PIPE

def ReadConfigFile(file_name):
    arg_dict = {}
    with open(file_name) as fp:
        lines = [i for i in fp.readlines() if not i.startswith('#') and i.strip()]
        for j in lines:
            if len(j.split(' ')) == 1:
                arg_dict[j] = ''
            else:
                arg_dict[j.split(' ')[0]] = j.split(' ')[1].strip()
    return arg_dict



class ProcessManager():
    name = 'default'
    prog = ''
    daemon = False
    opts = []
    
    def __init__(self, name, prog, pidfile='', daemon=True, opts=[]):
        self.name = name
        self.prog = prog
        self.configfile = '/etc/%s.conf'%self.name
        self.opts += opts
        
        if pidfile:
            self.pidfile = pidfile
        else:
            self.pidfile = '/var/run/%s/%s.pid'%(self.name, self.name)
        
        if daemon:
            self.opts.append('-d')
            self.opts += ['-P', self.pidfile]
            
    def config(self):
        config = ReadConfigFile(self.configfile)
        if '-m' in config:
            self.opts += ['-m', config['-m']]
        if '-u' in config:
            self.opts += ['-u', config['-u']]
        if '-p' in config:
            self.opts += ['-p', config['-p']]
        if '-c' in config:
            self.opts += ['-c', config['-c']]
        if '-l' in config:
            self.opts += ['-l', config['-l']]
        if '-v' in config:
            self.opts.append('-v')
        if '-vv' in config:
            self.opts.append('-vv')
        if '-k' in config:
            self.opts.append('-k')
        if '-M' in config:
            self.opts.append('-M')
        if '-r' in config:
            self.opts.append('-r')
    
    def touch_pid_dir(self):
       pid_dir = '/var/run/%s' %self.name
       config = ReadConfigFile(self.configfile)
       if not os.path.exists(pid_dir):
           touch_cmd = 'mkdir -p %s && chown %s:%s %s'%(pid_dir, config['-u'], config['-u'], pid_dir)
           try:
               subf_touch = Popen(touch_cmd, stdout=PIPE, stderr=PIPE, shell=True)
               err_touch = subf_touch.stderr.read()
               #if not err_touch:
                   #print 'The command of touch the dir:%s is OK!'%self.name
           except:
               err_touch = 'The command of touch the dir:%s could not be done!'%self.name
       if err_touch:
           for i in err_touch.split('\n'):
               print i
        
    def rm_pid_dir(self):
        pid_dir = '/var/run/%s'%self.name
        rm_cmd = ['rm', '-rf', pid_dir]
        try:
            subf_rm = Popen(rm_cmd, stdout=PIPE, stderr=PIPE)
            err_rm = subf_rm.stderr.read()
        except:
            err_rm = 'The command of remove the old pid dir could not be done!'
        if err_rm:
            for i in err_rm.split('\n'):
                print i
    
    def start(self):
        self.config()
        cmd = [self.prog] + self.opts
        print cmd
        self.touch_pid_dir()
        subf = Popen(cmd, stdout=PIPE, stderr=PIPE)
        cmd_err = subf.stderr.read()
        if not cmd_err:
            print cmd_err

    def stop(self):
        with open(self.pidfile, 'r') as fp:
            pid = fp.read().strip()
        cmd = ['kill', '-15', pid]
        try:
            subf = Popen(cmd, stdout=PIPE, stderr=PIPE)
            err = subf.stderr.read()
        except:
            err = 'The command of stop could not be done!'
        if err:
            for i in err.split('\n'):
                print i
        self.rm_pid_dir()

    def status(self):
        if os.path.exists(self.pidfile):
            with open(self.pidfile) as fp:
                pid = fp.read().strip()
            if pid:
                print 'The %s is running ,pid is %s'%(self.name, pid)
            else:
                print 'The %s is not running'%self.name
        else:
            print 'The %s is not running'%self.name

if __name__ == '__main__':
    pm = ProcessManager(name='memcached', prog='/usr/bin/memcached')
    if sys.argv[1] == 'start':
        pm.start()
    if sys.argv[1] == 'stop':
        pm.stop()
    if sys.argv[1] == 'status':
        pm.status()
        pm.status()
