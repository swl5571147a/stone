#!/usr/bin/env python

import os
import sys
import hashlib
import operator

def for_self(path):
	isfile,isdir,join = os.path.isfile,os.path.isdir,os.path.join
	lsdir = os.listdir(path)
	dirs = [i for i in lsdir if isdir(join(path,i))]
	files = [join(path,j) for j in lsdir if isfile(join(path,j))]
	for d in dirs:
#		files += for_self(join(path,d))
#	return files
		for (p,d,f) in for_self(join(path,d)):
			yield (p,d,f)
	yield path,dirs,files

file_dict = {}
if len(sys.argv) == 2:
	file_count = 0
	for i in for_self(sys.argv[1]):
		for j in i[2]:
			file_count += os.path.getsize(j)
			file_dict[j] = os.path.getsize(j)
	print 'the dir size is:%s' %file_count
	file_list = sorted(file_dict.iteritems(),key=operator.itemgetter(1),reverse=True)
	for z in file_list[:10]:
		print '%s\t%s' %(z[1],z[0])
else:
	print 'Error,You can only entry only one path'
