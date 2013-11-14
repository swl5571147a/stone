import os
import sys
from subprocess import Popen, PIPE



class ProcessManager():
    name = "default"
    prog = ""
    opts = []
    user = 'root'
    
    def __init__(self, name, prog, pidfile="", daemon=False, opts=[]):
        self.name = name
        self.prog = prog
        self.configfile = '/etc/sysconfig/%s' % self.name
        self.opts += opts 
        self.daemon = daemon

        if pidfile:
            self.pidfile = pidfile
        else:
            self.pidfile = "/var/run/%s.pid" % self.name

    def start(self):
        self.config()
        self.checkPIDfile()
        cmd = [self.prog] + self.opts 
        proc = Popen(cmd, stdout=PIPE, stderr=PIPE)
        print proc.pid
        if not self.daemon: self.checkPIDfile(proc.pid)
    
    def checkPIDfile(self, pid=""):
        with open(self.pidfile,'w') as fd:
            fd.write('%s'%pid)
        os.system("chown %s %s" % (self.user, self.pidfile))
    
    def config(self):
        if self.daemon:
            self.opts += ['-d', '-P', self.pidfile]
        config = readConfigFile(self.configfile)
        if 'USER' in config:
            self.opts += ['-u', config['USER']]
            self.user = config['USER']
        if 'CACHESIZE' in config:
            self.opts += ['-m', config['CACHESIZE']]
        if 'MAXCONN' in config:
            self.opts += ['-c', config['MAXCONN']]
        if 'PORT' in config:
            self.opts += ['-p', config['PORT']]

    def stop(self):
        pid = self.getpid()
        if checkPID(pid):
            os.kill(pid,15)
            os.remove(self.pidfile)

    def status(self):
        if checkPID(self.getpid()):
            print "running"
        else:
            print "not running"
        
    def getpid(self):
        return readPIDfile(self.pidfile)

def readConfigFile(f):
    with open(f) as fd:
        lines = [i for i in fd.readlines() if '=' in i]
        return dict(map(lambda x:[i.replace('"','').strip() for i in x.split('=')], lines))

def readPIDfile(f):
    if os.path.exists(f):
        with open(f) as fd:
            return int(fd.read().strip())

def checkPID(pid):
    return os.path.exists('/proc/%s'%pid)

if __name__ == "__main__":
    pm = ProcessManager(name='memcached', prog="/usr/bin/memcached", daemon=True)
    if sys.argv[1] == "start":
        pm.start()
    elif sys.argv[1] == "stop":
        pm.stop()
    elif sys.argv[1] == "status":
        pm.status()
    elif sys.argv[1] == "restart":
        pm.stop()
        pm.start()
    
