#!/usr/bin/env python2.7
#
#

import sys
from os import path
import os
import MySQLdb
DIRNAME = path.dirname(__file__)
OPSTOOLS_DIR = path.abspath(path.join(DIRNAME, '..'))
sys.path.append(OPSTOOLS_DIR)

from mysql import MySQLDConfig, getMyVariables
from optparse import OptionParser
from subprocess import Popen, PIPE

import time
import re
import datetime

MYSQL_DATA_DIR = "/var/mysqlmanager/data"
MYSQL_CONF_DIR = "/var/mysqlmanager/cnfs"
MYSQL_BACK_DIR = "/var/mysqlmanager/backup"

REPLICATION_PASS = "123qwe"
REPLICATION_USER = "repl"

ERROR_MSG = {
    0:'OK',
    1:'No config',
    2:'Not running',
    3:'No pid file',
}

ERROR_CODE = {
    'OK':0,
    'ERR_NOCFG':1,
    'ERR_NOTRUNNING':2,
    'ERR_NOPID':3,
}
def opts():
    parser = OptionParser(usage="usage: %prog options")
    parser.add_option("-c", "--cmd", 
                      dest="cmd", 
                      action="store",
                      default="check",)
    parser.add_option("-n", "--name", 
                      dest="name", 
                      action="store",
                      default="mysqlinstance",)
    parser.add_option("-p", "--port", 
                      dest="port", 
                      action="store",
                      default="3306",)
    parser.add_option("-t", "--type", 
                      dest="type", 
                      action="store",
                      default="master",
                      choices=("master","slave"))
    parser.add_option("-i", "--id", 
                      dest="serverid", 
                      action="store",
                      default="1")
    return parser.parse_args()


def mysql_install_db(cnf):
    cmd = "mysql_install_db --defaults-file=%s" % cnf.config 
    call_command(cmd)

def start_mysqld(cnf):
    cmd = "mysqld_safe --defaults-file=%s &" % cnf.config 
    call_command(cmd, shell=True, bg=True)

def call_command(cmd, shell=False, stdin=PIPE, stdout=PIPE, bg=False):
    import shlex
    if not shell: cmd = shlex.split(cmd)
    print cmd
    p = Popen(cmd, stdout=stdout, stderr=PIPE, stdin=stdin, shell=shell)
    if bg:
        p.poll()
    else:
        so, se = p.communicate()
        if p.returncode != 0:
            print "Err:", se
            sys.exit(1)

def init():
    for p in [MYSQL_CONF_DIR, MYSQL_DATA_DIR, MYSQL_BACK_DIR]:
        if not os.path.exists(p):
            os.makedirs(p)

def create_instance(name, port="3306", user='mysql', **kw):
    cnf_path = os.path.join(MYSQL_CONF_DIR, name + '.cnf')
    dat_path = os.path.join(MYSQL_DATA_DIR, name )
    pid_path = os.path.join(MYSQL_DATA_DIR, name , name + '.pid' )
    socket_path = os.path.join('/tmp', name + '.sock')
    if os.path.exists(cnf_path):
        mycnf = MySQLDConfig(cnf_path)
    else:
        mycnf = MySQLDConfig(cnf_path, user=user, port=port )
        mycnf.set_var('datadir', dat_path)
        mycnf.set_var('pid-file', pid_path)
        mycnf.set_var('socket', socket_path)
        for o,v in kw.items():
            mycnf.set_var(o,v)
        mycnf.save()
    if not os.path.exists(dat_path):
        mysql_install_db(mycnf)
    call_command('chown -R %s %s ' % (mycnf.mysqld_vars["user"], dat_path))
    if check_instance_status(name) != ERROR_CODE['OK']:
        start_mysqld(mycnf)

def check_instance_status(name):
    cnf_path = os.path.join(MYSQL_CONF_DIR, name + '.cnf')
    if os.path.exists(cnf_path):
        mycnf = MySQLDConfig(cnf_path)
        if 'pid-file' in mycnf.mysqld_vars:
            pid_path = mycnf.mysqld_vars['pid-file']
        else:
            pid_path = os.path.join(MYSQL_DATA_DIR, name , name + '.pid' )
        if os.path.exists(pid_path):
            with open(pid_path) as fd:
                pid = fd.read().strip()
            if os.path.exists('/proc/'+pid):
                return ERROR_CODE['OK']
            else:
                return ERROR_CODE['ERR_NOTRUNNING']
        else:
            return ERROR_CODE['ERR_NOPID']
    else:
        return ERROR_CODE['ERR_NOCFG']

def check_instance(name):
    ret = check_instance_status(name) 
    print name, ERROR_MSG[ret]

def readCnf(name):
    cnf_path = os.path.join(MYSQL_CONF_DIR, name + '.cnf')
    if os.path.exists(cnf_path):
        return MySQLDConfig(cnf_path)
        

def backup_instance(name):
    mycnf = readCnf(name)
    if mycnf:
        socket = mycnf.mysqld_vars['socket']
        now = datetime.datetime.now()
        timestamp = now.strftime('%Y-%m-%d_%H-%M-%S')
        bak = "%s_%s.sql" % (name, timestamp)
        backup_file = os.path.join(MYSQL_BACK_DIR, bak)
        #cmd = "mysqldump -S %s -uroot -A -x -F > %s " % (socket, backup_file)
        #call_command(cmd, shell=True)
        with open(backup_file, 'w') as fd:
            cmd = "mysqldump --master-data=2 -S %s -uroot -A -x -F " % (socket,)
            call_command(cmd, stdout=fd)

def check_socket(socket):
    times = 20
    for i in range(times):
        if os.path.exists(socket):
            return True
        else:
            time.sleep(1)
    return False

def restore_instance(name, port, sqlfile, **kw):
    create_instance(name, port=port, **kw)
    mycnf = readCnf(name)
    if mycnf:
        socket = mycnf.mysqld_vars['socket']
        if os.path.exists(sqlfile) and check_socket(socket):
            #cmd = "mysql -uroot -S %s < %s" % (socket, sqlfile)
            #call_command(cmd, shell=True)
            with open(sqlfile) as fd:
                cmd = "mysql -uroot -S %s " % (socket, )
                call_command(cmd, stdin=fd)

def connMySQLd(mc):
     host = mc.mysqld_vars['bind-address']
     user = 'root'
     port = int(mc.mysqld_vars['port'])
     conn = MySQLdb.connect(host, port=port, user=user)
     cur = conn.cursor()
     return cur

def execute_sql(cur, sql):
    cur.execute(sql)

def create_repl_user(name):
    mycnf = readCnf(name)
    if mycnf:
        sql = "GRANT REPLICATION SLAVE ON *.*  TO %s@'localhost'  IDENTIFIED BY '%s'" % (REPLICATION_USER, REPLICATION_PASS)
        socket = mycnf.mysqld_vars['socket']
        if check_socket(socket):
            cur = connMySQLd(mycnf)
            execute_sql(cur, sql)


def findLogPos(s):
    """
    >>> findLogPos("CHANGE MASTER TO MASTER_LOG_FILE='mysql-bin.000006', MASTER_LOG_POS=106;")
    ('mysql-bin.000006', 106)
    """
    rlog = re.compile(r"MASTER_LOG_FILE='(\S+)',",re.IGNORECASE)
    rpos = re.compile(r"MASTER_LOG_POS=(\d+),?",re.IGNORECASE)
    log = rlog.search(s)
    pos = rpos.search(s)
    if log and pos:
        return log.group(1), int(pos.group(1))
    else:
        return (None, None)

def findlogpos(sqlfile):
    with open(sqlfile) as fd:
        for l in fd:
            f,p = findLogPos(l)
            if f and p:
                return f,p


def slave_change_master(name,host,port,binfile, binpos):
    mycnf = readCnf(name)
    if mycnf:
        sql = """CHANGE MASTER TO
                MASTER_HOST='%s',
                MASTER_PORT=%s,
                MASTER_USER='%s',
                MASTER_PASSWORD='%s',
                MASTER_LOG_FILE='%s',
                MASTER_LOG_POS=%s;""" % (host,port,REPLICATION_USER, REPLICATION_PASS, binfile, binpos)
        socket = mycnf.mysqld_vars['socket']
        if check_socket(socket):
            cur = connMySQLd(mycnf)
            execute_sql(cur, sql)

def start_instance(name):
    conf_file = os.path.join(MYSQL_CONF_DIR, name + '.cnf')
    mycnf = MySQLDConfig(conf_file)
    if os.path.exists(conf_file):
        status = check_instance_status(name)
        if not status == 0:
            start_mysqld(mycnf)
        else:
            print "ERROR: This instance is runing , you cann't start again!"
            sys.exit(1)
    else:
        print ERROR_MSG[ERROR_CODE["ERR_NOCFG"]], ": No configuration for such instance"
        sys.exit(1)

def stop_instance(name):
    conf_file = os.path.join(MYSQL_CONF_DIR, name + '.cnf')
    if os.path.exists(conf_file):
        mycnf = MySQLDConfig(conf_file)
        if "socket" in mycnf.mysqld_vars:
            sock_file = mycnf.mysqld_vars['socket']
            status = check_instance_status(name)
            if status == 0:
                cmd = "mysqladmin -S %s shutdown" %sock_file
                call_command(cmd)
            else:
                print "ERROR: %s" %ERROR_MSG[status]
        else:
            print "ERROR: Counl not find the socket file in the configuration file: %s" %conf_file
    else:
        print ERROR_MSG[ERROR_CODE["ERR_NOCFG"]], ": No configuration for such instance"
        sys.exit(1)

def main():
    init()
    opt, args = opts()
    name = opt.name
    port = opt.port
    if opt.cmd == "create":
        if opt.type == "master":
            mysqld_options = {'server-id':opt.serverid, 'log-bin':'mysql-bin'}
            create_instance(name, port=port, **mysqld_options)
            create_repl_user(name)
        elif opt.type == "slave":
            sqlfile = args[2]
            master_host = args[0]
            master_port = args[1]
            print opt
            mysqld_options = {'server-id':opt.serverid,'skip-slave-start':None,'replicate-ignore-db':'mysql'}
            restore_instance(name, port, sqlfile,**mysqld_options)
            binlog_file, binlog_pos = findlogpos(sqlfile)
            slave_change_master(name, master_host, master_port, binlog_file, binlog_pos)
    elif opt.cmd == "backup":
        backup_instance(name)
    elif opt.cmd == "check":
        check_instance(name)
    elif opt.cmd == "restore":
        sqlfile = args[0]
        restore_instance(name, port, sqlfile)
    elif opt.cmd == "start":
        start_instance(name)
    elif opt.cmd == "stop":
        stop_instance(name)

if __name__ == "__main__":
    main()
