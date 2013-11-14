#!/usr/bin/env python

class ProcessManager():
    name = 'default'
    prog = ''
    daemon = False
    opts = ['-u','nobody']

    def __init__(self,name,prog,pidfile='',daemon=True,opts=[]):
        self.name = name
        self.prog = prog
        self.configure = '/etc/sysconfigure/%s' % self.name
        self.opts += opts

        if pidfile:
            self.pidfile = pidfile
        else:
            self.pidfile = '/var/run/%s.pid' % self.name
        if daemon:
            self.opts.append('-d')
            self.opts += ['-P',self.pidfile]

    def start(self):
        cmd = [self.prog] + self.opts
        print cmd
        proc = Popen(cmd,stdout=PIPE,stderr=PIPE)
        print proc.stderr.read()

    def config(self):
        config = readConfigFile(self.configfile)

def readConfigFile(f):
    with open(f) as fd:
        lines = [i for i in fd.readlines() if '=' in i]
        return dict(map(lambda x:[]))
