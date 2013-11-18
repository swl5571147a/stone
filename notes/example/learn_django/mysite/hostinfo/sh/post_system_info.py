import platform
from subprocess import Popen,PIPE

info = {}

def get_hostname_os():
    info['hostname'] = platform.node()
    info['osver'] = platform.platform()

def get_memory():
    with open('/proc/meminfo') as fp:
        for i in fp.readlines():
            if i.startswith('MemTotal'):
                info['memory'] = i.split(':').[1]split()[0].strip()

def get_cpu():
    with open('/proc/cpuinfo') as fp:
        for i in fp.readlines():
            if i.startswith('model name '):
                info['cpu_model'] = i.split(':')[1]
            if i.startswith('cpu cores'):
                info['cpu_num'] = int(i.split(':')[1])

def get_hardware():
    subf = Popen(['dmidecode'],stdout=PIPE,stderr=PIPE)
    data = subf.stdout.read()
