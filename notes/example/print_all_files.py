#!/usr/bin/env python

import os
import sys
import hashlib_test

def print_all_files(path,file_list):
    isfile,isdir,join = os.path.isfile,os.path.isdir,os.path.join
    lsdir = os.listdir(path)
    dirs = [i for i in lsdir if isdir(join(path,i))]
    files = [j for j in lsdir if isfile(join(path,j))]
    for d in dirs:
        print_all_files(join(path,d),file_list)
    for f in files:
    #    m = hashlib.md5()
    #    fd = open(join(path,f))
    #    data = fd.read()
    #    m.update(data)
    #    print join(path,f),':',m.hexdigest()
    #    print join(path,f),':',hashlib_test.md5sum(join(path,f))
        file_list.append(join(path,f))
    #return file_list

if __name__ == '__main__':
    flst = []
    print_all_files(sys.argv[1],file_list=flst)
    for i in flst:
        print i

