#!/usr/bin/env python

import os
import sys
import hashlib_test

def print_all_files(path):
	isfile,isdir,join = os.path.isfile,os.path.isdir,os.path.join
	lsdir = os.listdir(path)
	dirs = [i for i in lsdir if isdir(join(path,i))]
	files = [join(path,j) for j in lsdir if isfile(join(path,j))]
	for d in dirs:
		files += print_all_files(join(path,d))
	return files

if __name__ == '__main__':
	for i in print_all_files(sys.argv[1]):
		print i
