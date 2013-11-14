#!/usr/bin/env python

import sys
from subprocess import Popen, PIPE



class ProcessManager():
    name = "default"
    prog = ""
    daemon = False
    opts = []
    
    def __init__(self, name, prog, pidfile="", daemon=True, opts=[]):
        self.name = name
        self.prog = prog
        self.configfile = '/etc/sysconfig/%s' % self.name
        self.opts += opts 
   
        if pidfile:
            self.pidfile = pidfile
        else:
            self.pidfile = "/var/run/%s.pid" % self.name
        if daemon:
            self.opts.append('-d')
            self.opts += ['-P', self.pidfile]

    def start(self):
        self.config()
        cmd = [self.prog] + self.opts 
        print cmd 
        proc = Popen(cmd, stdout=PIPE, stderr=PIPE)
        #print proc.stderr.read()
    
    def status(self):
        if os.path.exists(self.pidfile):
            fp = open(self.pidfile)
            pid = fp.read().strip()
            fp.close()
            return pid
        else:
            return '%s is not running....'%self.name

    def stop(self):
        

    def config(self):
        config = readConfigFile(self.configfile)
        if 'USER' in config:
            self.opts += ['-u', config['USER']]
        if 'CACHESIZE' in config:
            self.opts += ['-m', config['CACHESIZE']]
        if 'MAXCONN' in config:
            self.opts += ['-c', config['MAXCONN']]
        if 'PORT' in config:
            self.opts += ['-p', config['PORT']]

def readConfigFile(f):
    with open(f) as fd:
        lines = [i for i in fd.readlines() if '=' in i]
        return dict(map(lambda x:[i.replace('"','').strip() for i in x.split('=')], lines))

if __name__ == "__main__":
    pm = ProcessManager(name='memcached', prog="/usr/bin/memcached")
    if sys.argv[1] == "start":
        pm.start()
