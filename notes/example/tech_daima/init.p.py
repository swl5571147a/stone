import sys
from rc import ProcessManager

class PM(ProcessManager):

    def config(self):
        pass


if __name__ == "__main__":
    pm = PM(name='simpleppy', prog="/root/p.py")
    if sys.argv[1] == "start":
        pm.start()
    elif sys.argv[1] == "stop":
        pm.stop()
    elif sys.argv[1] == "status":
        pm.status()
    elif sys.argv[1] == "restart":
        pm.stop()
        pm.start()
    
