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
       if not os.path.exists(pid_dir):
           touch_cmd = ['mkdir', '-p', self.name]
    
    def start(self):
        self.config()
        cmd = [self.prog] + self.opts
        print cmd
        subf = Popen(cmd, stdout=PIPE, stderr=PIPE)
        cmd_err = subf.stderr.read()
        if not cmd_err:
            print cmd_err

if __name__ == '__main__':
    pm = ProcessManager(name='memcached', prog='/usr/bin/memcached')
    if sys.argv[1] == 'start':
        pm.start()
