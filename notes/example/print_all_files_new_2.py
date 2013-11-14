#!/usr/bin/env python

import os
import sys
import hashlib_test
import hashlib

def print_all_files(path):
	isfile,isdir,join = os.path.isfile,os.path.isdir,os.path.join
	lsdir = os.listdir(path)
	dirs = [i for i in lsdir if isdir(join(path,i))]
	files = [join(path,j) for j in lsdir if isfile(join(path,j))]
	for d in dirs:
		for (p,d,f) in print_all_files(join(path,d)):
			yield (p,d,f)
	yield (path,dirs,files)

if __name__ == '__main__':
	file_list = []
	md = hashlib.md5()
	md2 = hashlib.md5()
	tt = ''
	file_size = 0
	for i in print_all_files(sys.argv[1]):
		file_list += i[2]
	for f in file_list:
		print '%s  %s' %(hashlib_test.md5sum(f),f)
		tt += '%s  %s' %(hashlib_test.md5sum(f),f)
		print tt
		fd = open(f)
		data = fd.read()
		md.update(data)
		fd.close()
		file_size += os.path.getsize(f)
		md2.update(hashlib_test.md5sum(f))
	print 'This dir md5 is:%s' %md2.hexdigest()
	print 'all files size is:%s' %file_size
	print hashlib.md5(tt).hexdigest()
