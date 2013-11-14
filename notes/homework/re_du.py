#!/usr/bin/env python
#-*- coding:utf-8 -*-

import os
import sys
import operator

#class File_Type(object):
#    '''获取文件名称/路径/类型/大小'''
#    def __init__(self,file_name,file_type,file_size):
#    self.file_name = file_name
#    self.file_type = file_type
#    self.file_size = file_size

def get_all(path):
    '''获取目录下所有的对象，包括目录/路径/文件'''
    isfile,isdir,join = os.path.isfile,os.path.isdir,os.path.join
    lsdir = os.listdir(path)
    dirs = [i for i in lsdir if isdir(join(path,i))]
    files = [join(path,j) for j in lsdir if isfile(join(path,j))]
    for ds in dirs:
        for x in get_all(join(path,ds)):
            yield x
    yield path,dirs,files

def get_all_files(path):
    '''获取目录下所有的文件'''
    files_list = []
    for i in get_all(path):
        for j in i[2]:
            files_list.append(j)
    yield files_list

def get_files_size(path):
    '''获取目录下所有文件的大小，并计算总和'''
    file_count = 0
    file_dict = {}
    for i in get_all_files(path):
        for j in i:
            file_dict[j] = os.path.getsize(j)
            file_count += os.path.getsize(j)
    yield file_count,file_dict

def get_type(path):
    '''字典记录文件后缀及其行数，最后最字典进行按行数排序。
    字典中suff表示无后缀，如‘aaa’；
    字典中对多后缀文件不处理，如'aaa.tar.gz';
    '''
    type_list = {}
    for i in get_all_files(path):
        for j in i:
            file_name = os.path.split(j)[1]
            if file_name.count('.') == 0:
                fp = open(j)
                data = fp.read()
                if type_list.has_key('suff'):
                    type_list['suff'] += data.count('\n')
                else:
                    type_list['suff'] = data.count('\n')
                fp.close()
            elif file_name.count('.') == 1:
                file_type = os.path.splitext(file_name)[1]
                fp = open(j)
                data = fp.read()
                if not type_list.has_key(file_type):
                    type_list[file_type] = data.count('\n')
                else:
                    type_list[file_type] += data.count('\n')
                fp.close()
            else:
                pass
    return type_list

def sort_top10(d):
    '''对字典排序，按照字典value值进行排序，如果有超过十个key
    则输出top 10，如果没有十个key，则输出全部
    '''
    if len(d) > 10:
        return sorted(d.iteritems(),key=operator.itemgetter(1),reverse=True)[:10]
    else:
        return sorted(d.iteritems(),key=operator.itemgetter(1),reverse=True)

if __name__ == '__main__':
    print '*' * 50
    print '文件大小统计：'
    for i in get_files_size(sys.argv[1]):
        for (file_name,file_size) in i[1].items():
            print '%s\t%s' %(file_size,file_name)
        print '%s\tTotal' %i[0]
    print '*' * 50
    print '不同文件类型行数top 10:'
    for i in sort_top10(get_type(sys.argv[1])):
        print '%s\t%s' %(i[1],i[0])
    
