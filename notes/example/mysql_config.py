#!/usr/bin/env python

from ConfigParser import ConfigParser
import os

def getMyVariables(cur):
    pass

class MySQLConfig(ConfigParser):
    def __init__(self, config, **kw):
        ConfigParser.__init__(self, allow_no_value=True)
        self.config = config
        self.mysqld_vars = {}
        if os.path.exists(self.config):
            self.read(self.config)
            self.get_mysqld_vars()
        else:
            self.set_mysqld_default_vars()
        self.set_mysqld_vars(kw)

    def set_mysqld_vars(self, kw):
        for k, v in kw.items():
            self.mysqld_vars[k] = v

    def set_var(self, k, v):
        self.mysqld_vars[k] = v

    def get_mysqld_vars(self):
        options = self.options('mysqld')
        rst = {}
        for o in options:
            rst[o] = self.get('mysqld', o)
        self.set_mysqld_vars(rst)

    def set_mysqld_default_vars(self):
        defaults = {
            "user": "mysql",
            "pid-file": "/var/run/mysqld/mysqld.pid",
            "socket": "/var/lib/mysql/mysql.sock",
            "port": "3306",
            "basedir": "/usr",
            "datadir": "/tmp/mysql",
            "tmpdir": "/tmp",
            "skip-external-locking": None,
            "bind-address": "127.0.0.1",
            "key_buffer": "16M",
            "max_allowed_packet": "16M",
            "thread_stack": "192K",
            "thread_cache_size": "8",
            "myisam-recover": "BACKUP",
            "query_cache_limit": "1M",
            "query_cache_size": "16M",
            "log_error": "/var/log/mysqld.log",
            "expire_logs_days": "10",
            "max_binlog_size": "100M",
        }
        self.set_mysqld_vars(defaults)

    def save(self):
        if not self.has_section('mysqld'):
            self.add_section('mysqld')
        for k, v in self.mysqld_vars.items():
            self.set('mysqld', k, v)
        with open(self.config, 'w') as fd:
            self.write(fd)

def main():
    mc = MySQLConfig("/tmp/my1.cnf", max_connection=200, user="mysql123")
    mc.set_var('skip-slave-start', None)
    mc.save()

if __name__ == '__main__':
    main()