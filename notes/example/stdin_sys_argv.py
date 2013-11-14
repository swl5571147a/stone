#!/usr/bin/env python
#coding:utf-8

import sys

def get_count(data):
	charts = len(data)
	words = len(data.split())
	lines = data.count("\n")

	return charts,words,lines

if len(sys.argv) == 1:
	data = sys.stdin.read()
	print "charts:%s   words:%s   lines:%s" %get_count(data)
elif len(sys.argv) >= 2:
	t_charts = 0
	t_words = 0
	t_lines = 0
	file_list = sys.argv[1:]
	if file_list[0] in ('-c','c','-w','w','-l','l'):
		argvment = file_list[0]
		file_list.remove(argvment)
	elif file_list[len(file_list)-1] in ('-c','c','-w','w','-l','l'):
		argvment = file_list[len(file_list)-1]
		file_list.remove(argvment)
	else:
		argvment = ""

	if argvment in ('-c','c','-w','w','-l','l'):
		for filename in file_list:
			data = open(filename).read()
			charts,words,lines = get_count(data)
			t_charts += charts
			t_words += words
			t_lines += lines
			if argvment in ('-c','c'):
				print "filename:%s    charts:%s" %(filename,charts)
			elif argvment in ('-w','w'):
				print "filename:%s    charts:%s" %(filename,words)
			elif argvment in ('-l','l'):
				print "filename:%s    lines:%s" %(filename,lines)
			else:
				print "argvment error!"
		if argvment in ('-c','c'):
			print "Total:%s" %t_charts
		elif argvment in ('-w','w'):
			print "Total:%s" %t_words
		elif argvment in ('-l','l'):
			print "Total:%s" %t_lines
	else:
		for filename in file_list:
			data = open(filename).read()
			print "filename:%s   charts:%s   words:%s   lines:%s" %(filename,get_count(data)[0],get_count(data)[1],get_count(data)[2])
			t_charts += get_count(data)[0]
			t_words += get_count(data)[1]
			t_lines += get_count(data)[2]
		print "Total   charts:%s   words:%s   lines:%s" %(t_charts,t_words,t_lines)
#elif len(sys.argv) == 3:
#	arg = sys.argv[1]
#	data = open(sys.argv[2]).read()
#	if arg in ("-c","c"):
#		print "charts:%s" %get_count(data)[0]
#	elif arg in ("-w","w"):
#		print "words:%s" %get_count(data)[1]
#	elif arg in ("-l","l"):
#		print "lines:%s" %get_count(data)[2]
#	else:
#		print "Bad cmd argument!"
else:
	print "sorry,i can't do it!"
	print sys.argv

