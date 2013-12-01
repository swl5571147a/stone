#!/usr/bin/env python

import paramiko,os,sys,commands,time
from subprocess import Popen, PIPE
import shlex

#set the default configure and argvs
current_time = time.strftime('%Y-%m-%d-%H-%M-%S',time.localtime(time.time()))
conf = {'path_mcu':'/home/broad/sunwenlong/iserver-mcu/medooze',
        'path_mcuWeb':'',
        'path_siremis':'/home/broad/sunwenlong/iserver-sipserver',
        'path_source':'/home/broad/sunwenlong/source',
        'port':22,
        'remote_ip':'192.168.1.100',
        'root':'broadeng',
        'broad':'broad123',
        'path_sql':'/home/broad/sunwenlong/iserver-sipserver/config'
}

def ssh_get_source(remote_ip,port,user,passwd):
    '''set the ssh-connect for gettiing the source'''
    ssh = paramiko.SSHClient()
    ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
    ssh.connect(remote_ip,port,user,passwd)
    return ssh

def ssh_down_load(remote_ip,port,user,passwd):
    '''set the ssh-connect for down load the tar_source'''
    ssh = paramiko.Transport((remote_ip,port))
    ssh.connect(username=user,password=passwd)
    return ssh

def git_update_tar(ssh,path,file_name):
    '''To update the git from gitserver and tar the target dir to filename-current_time.tar.gz'''
    cmd = 'cd %s && git pull && tar zcvf %s-%s.tar.gz %s'%(path,file_name,current_time, file_name)
    try:
        stdin,stdout,stderr = ssh.exec_command(cmd)
        print '%s backup OK'%file_name
    except:
        print 'Error! %s backup error'%file_name
        
    if not len(stderr.read()) == 0:
        print stderr.read()

    ssh.close()

def scp_source(ssh,path,file_name):
    '''From the source to down load the tar file'''
    sftp = paramiko.SFTPClient.from_transport(ssh)
    remote_path = '%s/%s-%s.tar.gz'%(path,file_name,current_time)
    local_path = '%s/%s-%s.tar.gz'%(conf['path_source'],file_name,current_time)
    try:
        s = sftp.get(remote_path,local_path)
        print 'OK! %s download sucessfully!'%file_name
    except:
        print 'Error! %s could not download!'%file_name
    
    ssh.close()

def clean_source(ssh,path,file_name):
    '''To clean the tar file in the source dir'''
    cmd = 'rm -f %s/%s-%s.tar.gz'%(path,file_name,current_time)
    stdin,stdout,stderr = ssh.exec_command(cmd)

    if not stderr.readlines():
        print '%s-%s.tar.gz clean up from remote'%(file_name,current_time)
    else:
        print 'Error! %s-%s.tar.gz clean up error'%(file_name,current_time)

def tar_zxvf(file_name):
    '''To tar zxvf the tar_file_name '''
    dir_path = os.path.join(conf['path_source'], file_name)
    err_rm = clean_old_dir(dir_path) 
    print_err(err_rm)

    tar_path = os.path.join(conf['path_source'], '%s-%s.tar.gz')%(file_name,current_time)
    tar_file = '%s-%s.tar.gz'%(file_name,current_time)
    tar_cmd = 'cd %s && tar zxvf %s'%(conf['path_source'], tar_file)
    if os.path.exists(tar_path):
        try:
            subf_tar = Popen(tar_cmd, stdout=PIPE, stderr=PIPE, shell=True)
            err_tar = subf_tar.stderr.read()
            if not err_tar:
                print 'tar zxvf %s is OK!'%tar_file
        except:
            err_tar = 'Error! The command of tar zxvf %s clould not be done!Please check it!'%(tar_file)
    else:
        print 'Error! The file of %s is not exists!Please check it in dir:%s'%(file_name, conf['path_source'])

    print_err(err_tar)

def mcu_make():
    '''To make the new mcu and replace the old mcu'''
    make_path = os.path.join(conf['path_source'], 'mcu')
    print 'It will take some minutes,Please wait ......'
    if not os.path.exists(make_path):
        print 'Error! The dir mcu clould not be found! Please chech it in dir:/home/broad/sunwenlong/source '
    else:
        make_cmd = 'cd %s && sudo make'%make_path
        try:
            subf = Popen(make_cmd, stdout=PIPE, stderr=PIPE, shell=True)
            err_make = subf.stderr.read()
            if not err_make:
                print 'make mcu OK!'
        except:
            err_make = 'Error! The mcu_make_cmd cloud not be done!'
    print_err(err_make)
    
    make_mcu_path = os.path.join(make_path, 'bin/release')
    new_mcu = os.path.join(make_mcu_path, 'mcu')
    old_mcu_path = '/usr/local/bin'
    old_mcu = '/usr/local/bin/mcu'
    if os.path.exists(new_mcu):
        rm_cmd = 'rm -f %s'%old_mcu
        cp_cmd = 'cp %s %s'%(new_mcu, old_mcu_path)
        try:
            subf_rm = Popen(rm_cmd, stdout=PIPE, stderr=PIPE, shell=True)
            subf_cp = Popen(cp_cmd, stdout=PIPE, stderr=PIPE, shell=True)
            err_rm = subf_rm.stderr.read()
            err_cp = subf_cp.stderr.read()
            if not err_rm:
                print 'OK! The command of remove the old mcu is OK!'
            if not err_cp:
                print 'OK! Copy the new mcu to /usr/local/bin is OK!'
        except:
            err_rm = 'Error! The command of remove the old mcu could not be done!Please check it!'
            err_cp = 'Error! The command of copy the new mcu to /usr/local/bin could not be done!Please check it!'
    else:
        print 'Warning! The target file mcu is not exists,Please it!'
    print_err(err_rm)
    print_err(err_cp)
    
def restart_service(target_service):
    '''To restart the service of target_service'''
    re_cmd = ['service', target_service, 'restart']
    try:
        subf_re = Popen(re_cmd, stdout=PIPE, stderr=PIPE)
        err_re = subf_re.stderr.read()
        if not err_re:
            print 'OK! The command of restart the service %s is OK!'%target_service
    except:
        err_re = 'Error! The command of restart the service %s colud not be done!'%target_service
    print_err(err_re)

def print_err(s):
    '''To print the error if there is error'''
    if s:
        for i in s.split('\n'):
            print i

def clean_old_dir(dir_path):
    '''To clean the old dir for the new dir using'''
    if os.path.exists(dir_path):
        cmd = ['rm', '-rf', dir_path]
        try:
            subf = Popen(cmd, stdout=PIPE, stderr=PIPE)
            err = subf.stderr.read()
        except:
            err = 'Error! The command of cleaning the old dir which is %s is not be done!Please it!'%dir_path
    return err

def replace_siremis(dir_name):
    '''To remove the old siremis dir, and copy the new dir of siremis to /var/www'''
    #remove the old siremis dir
    dir_path = os.path.join('/var/www', dir_name)
    if os.path.exists(dir_path):
        rm_cmd = ['rm', '-rf', dir_path]
        try:
            subf_rm = Popen(rm_cmd, stdout=PIPE, stderr=PIPE)
            err_rm = subf_rm.stderr.read()
            if not err_rm:
                print 'OK! The command of remove the dir : %s is OK!'%dir_name
        except:
            err_rm = 'Error! The command of remove the dir : %s colud not be done!Please chech it!'%dir_name
    print_err(err_rm)
    
    #to cp the new siremis to /var/www
    src_path = os.path.join(conf['path_source'], dir_name)
    cp_cmd = ['cp', '-r', src_path, '/var/www']
    try:
        subf_cp = Popen(cp_cmd, stdout=PIPE, stderr=PIPE)
        err_cp = subf_cp.stderr.read()
        if not err_cp:
            print 'OK! The command of copy the dir : %s to /var/www is OK!'%dir_name
    except:
        err_cp = 'Error! The command of copy the dir : %s to /var/www colud not be done!Please check it!'%dir_name
    print_err(err_cp)
    
    #to chown the owner of the dir siremis
    if os.path.exists(dir_path):
        ch_cmd = ['chown','-R',  'www-data:www-data', dir_path]
        try:
            subf_ch = Popen(ch_cmd, stdout=PIPE, stderr=PIPE)
            err_ch = subf_ch.stderr.read()
            if not err_ch:
                print 'OK! The command of chown the %s to www-data is OK!'%dir_name
        except:
            err_ch = 'Error! The command of chown the %s to www-data colud not be done!Please check it!'%dir_name
    print_err(err_ch)

def purge_kernel(kernel):
    '''purge kernel 3.9.5 and 3.11.6'''
    cmd = ['apt-get','purge',kernel]
    try:
        subf = Popen(cmd,stderr=PIPE)
        err = subf.stderr.read()
    except:
        err = 'Error! The command of purge %s could not be done!'%kernel
    if err:
        print err

def remove_rubbish(path):
    '''remove rubbish'''
    cmd = 'rm -Rf %s' %path
    try:
        subf = Popen(cmd,stderr=PIPE,shell=True)
        err = subf.stderr.read()
    except:
        err = 'Error! The command of remove %s could not be done!'%path
    if err:
        print err

def get_file_md5(file_path):
    '''Get the file md5'''
    if os.path.exists(file_path):
        cmd = ['md5sum',file_path]
        try:
            subf = Popen(cmd,stderr=PIPE,stdout=PIPE)
            data = subf.stdout.read()
            err = subf.stderr.read()
        except:
            data = ''
            err = 'Error! The command of md5sum %s could not be done!'%file_path
        if err:
            print err
        if data:
            md5_value = data.split()[0].strip()
        else:
            print 'Warning! Could not get the %s md5 value!'%file_path
    else:
        md5_value = ''
        print 'Warning! The %s is not exists!'%file_path
    return md5_value

def update_sql(db_name,sql_bak_name):
    '''update the mysql table'''
    md5_file = '%s/md5.txt'%conf['path_source']
    if os.path.exists(md5_file):
        with open(md5_file,'r') as fp:
            old_md5 = fp.read().strip()
    else:
        old_md5 = ''

    ssh = ssh_down_load(conf['remote_ip'],conf['port'],'root',conf['root'])
    sftp = paramiko.SFTPClient.from_transport(ssh)
    remote_path = '%s/%s'%(conf['path_sql'],sql_bak_name)
    local_path = '%s/%s'%(conf['path_source'],sql_bak_name)
    try:
        sftp.get(remote_path,local_path)
        print 'OK! %s download sucessfully!'%sql_bak_name
    except:
        print 'Error! %s could not download!'%sql_bak_name
    ssh.close()

    if os.path.exists(local_path):
        new_md5 = get_file_md5(local_path)
    else:
        new_md5 = ''
        print 'Error! The file of md5 %s is not exists!'%local_path

    if not old_md5 == new_md5:
        cmd = 'mysql -uroot -pbroadeng %s < %s/%s' %(db_name,conf['path_source'],sql_bak_name)
        try:
            subf = Popen(cmd,stderr=PIPE,shell=True)
            err = subf.stderr.read()
        except:
            err = 'Error! The command of update of the mysql table %s could not be done!'%db_name
        if err:
            print err
        restart_service('mysql')
        restart_service('mcuWeb')

        with open(md5_file,'w') as fp_w:
            fp_w.write(new_md5)

def close_sudo():
    '''close sudo users'''
    cmd = ['cp','-f','/etc/sudoers.bak','/etc/sudoers']
    try:
        subf = Popen(cmd,stderr=PIPE)
        err = subf.stderr.read()
    except:
        err = 'Error! The command of modify the sudoers could not be done!'
    if err:
        print err

def main():
    #update the mcu from git and tar it to tar_file
    git_update_tar(ssh_get_source(conf['remote_ip'],conf['port'],'broad',conf['broad']),conf['path_mcu'],'mcu')
    time.sleep(1)
    #down load the mcu tar_file
    scp_source(ssh_down_load(conf['remote_ip'],conf['port'],'root',conf['root']),conf['path_mcu'],'mcu')
    time.sleep(1)
    #clean the source
    clean_source(ssh_get_source(conf['remote_ip'],conf['port'],'broad',conf['broad']),conf['path_mcu'],'mcu')
    time.sleep(1)
    #tar zxvf mcu
    tar_zxvf('mcu')
    time.sleep(1)
    #make mcu and replace the old mcu
    mcu_make()
    time.sleep(1)
    #restart the mcu
    restart_service('mediamixer')

    #update the siremis from git and tar it to tar_file
    git_update_tar(ssh_get_source(conf['remote_ip'], conf['port'], 'broad', conf['broad']), conf['path_siremis'], 'siremis-4.0.0')
    time.sleep(1)
    #down load the siremis tar_file
    scp_source(ssh_down_load(conf['remote_ip'], conf['port'], 'root', conf['root']), conf['path_siremis'], 'siremis-4.0.0')
    time.sleep(1)
    #clean the source
    clean_source(ssh_get_source(conf['remote_ip'],conf['port'],'broad',conf['broad']),conf['path_siremis'],'siremis-4.0.0')
    time.sleep(1)
    #tar zxvf mcu
    tar_zxvf('siremis-4.0.0')
    time.sleep(1)
    #remove the old siremis and copy the new siremis to /var/www
    replace_siremis('siremis-4.0.0')
    time.sleep(1)
    #restart the apache2 to make sure it work
    restart_service('apache2')

    #update mysql table
    update_sql('kamailio','kamailio.sql')

    #purge the kernel
    purge_kernel('linux-image-3.11.6-031106-generic')
    purge_kernel('linux-image-3.9.5-030905-generic')

    #close sudoers
    close_sudo()

    #remove the rubbish
    remove_rubbish('/opt/*')
    remove_rubbish('/usr/local/src/*')

if __name__ == '__main__':
    main()