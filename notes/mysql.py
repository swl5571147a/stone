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
        for k,v in kw.items():
            self.mysqld_vars[k] = v

    def set_var(self,k,v):
        self.mysqld_vars[k] = v
         
    def get_mysqld_vars(self):
        options = self.options('mysqld')
        rst = {}
        for o in options:
            rst[o] = self.get('mysqld',o)
        self.set_mysqld_vars(rst)

    def set_mysqld_defaults_var(self):
        defaults = {
           "port":"3306",
           "slow-query-log-file":"/home/mysql/log/MysqlQuery.log",
           "long_query_time":"0.5",
           "slow_query_log":"1",
           "--skip-external-locking":None,
           "skip-locking":None,
           "join_buffer_size":"128M",
           "sort_buffer_size":"2M",
           "read_rnd_buffer_size":"16M",
           "key_buffer_size":"1024M",
           "max_allowed_packet":"8M",
           "innodb_buffer_pool_size":"20G",
           "skip-name-resolve":None,
           "back_log":"50",
           "max_connections":"1000",
           "max_connect_errors":"100",
           "table_open_cache":"2048",
           "binlog_cache_size":"1M",
           "max_heap_table_size":"64M",
           "read_buffer_size":"2M",
           "thread_cache_size":"8",
           "thread_concurrency":"8",
           "query_cache_size":"64M",
           "query_cache_limit":"2M",
           "ft_min_word_len":"4",
           "thread_stack":"192K",
           "tmp_table_size":"64M",
           "binlog_format":"mixed",
           "innodb_additional_mem_pool_size":"16M",
           "innodb_write_io_threads":"8",
           "innodb_read_io_threads":"8",
           "innodb_thread_concurrency":"16",
           "innodb_flush_log_at_trx_commit":"2",
           "innodb_log_buffer_size":"8M",
           "innodb_log_file_size":"512M",
           "innodb_log_files_in_group":"3",
           "innodb_max_dirty_pages_pct":"90",
           "innodb_lock_wait_timeout":"30",
           "sql_mode":"NO_ENGINE_SUBSTITUTION,STRICT_TRANS_TABLES",
           "skip_locking":None, 
        }
        self.set_mysqld_vars(defaults)
    
    def save(self):
        if not self.has_section('mysqld'):
            self.add_section('mysqld')
        for k,v in self.mysqld_vars.items():
            self.set('mysqld',k,v)
        with open(self.config,'w') as fd:
            self.write(fd)  

mc = MysqlConfig('/tmp/my3.cnf',max_connections=200,port='3310')
mc.set_var('max_connections',300)
mc.save()
