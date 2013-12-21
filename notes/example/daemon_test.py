import os
import sys
import atexit
import signal

def run():
    pass

def del_pid(name):
    pass

def write_pid(name):
    pass

def daemon(name):
    try:
        pid = os.fork()
        if pid:
            sys.exit(0)
    except OSError, msg:
        print 'fork #1 fail'
        sys.exit(1)

    os.chdir('/')
    os.setsid()
    os.umask(0)

    try:
        pid = os.fork()
        if pid:
            print "pid is %s" % pid
            sys.exit(0)
    except OSError, msg:
        print 'fork #2 fail'
        sys.exit(1)

    atexit.register(del_pid, name)
    signal.signal(signal.SIGTERM, sys.exitfunc)

if __name__ == "__main__":
    daemon()