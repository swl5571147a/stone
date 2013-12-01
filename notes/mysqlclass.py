from ConfigParser import ConfigParser
import os

class MysqlConfig(ConfigParser):
    def __init__(self,config,**kw):
        ConfigParser.__init__(self,allow_no_value=True) 
        self.config = config
        self.mysqld_vars = {}
        if os.path.exists(self.config):
            self.read(self.config)
            self.get_mysqld_vars()
        else:
            self.set_mysqld_defaults_var()
        self.set_mysqld_vars(kw)

    def set_mysqld_vars(self,kw):

    def set_var(self,k,v):
         
    def get_mysqld_vars(self):

    def set_mysqld_defaults_var(self):
        defaults = {
           "port":"3306",
        }
    
    def save(self):

mc = MysqlConfig('/tmp/my3.cnf',max_connections=200,port='3310')
mc.set_var('max_connections',300)
mc.save()
