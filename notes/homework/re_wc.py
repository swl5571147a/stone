#!/usr/bin/env python
#coding:utf-8

import os
import sys
import time
from optparse import OptionParser

def get_count(data):
	charts = len(data)
	words = len(data.split())
	lines = data.count("\n")

	return charts,words,lines

def need_print(p,charts,words,lines,filename):
	if p.chart == True:
		if charts < 10:
			print "charts:%s\t\t" %charts,
		else:
			print "charts:%s\t" %charts,
	if p.word == True:
		if words < 10:
			print "words:%s\t\t" %words,
		else:
			print "words:%s\t" %words,
	if p.line == True:
		if lines < 10:
			print "lines:%s\t\t" %lines,
		else:
			print "lines:%s\t" %lines,
	print filename

def inst_args():
	parser = OptionParser('%prog [-c] [-w] [-l] [-n] [-h] can be used')
	parser.add_option('-c','--chart',dest='chart',action='store_true',default=False,help='count the charts')
	parser.add_option('-w','--word',dest='word',action='store_true',default=False,help='count the words')
	parser.add_option('-l','--line',dest='line',action='store_true',default=False,help='count the lines')
	parser.add_option('-n','--no-total',dest='nototal',action='store_true',default=False,help='no print the total')

	p,args = parser.parse_args()
	return p,args

if __name__ == '__main__':
	p,args = inst_args()

	if not (p.chart or p.word or p.line):
		p.chart,p.word,p.line = True,True,True

 	if len(args) > 0:
		t_charts,t_words,t_lines = 0,0,0
		for filename in args:
			if os.path.isdir(filename) or os.path.islink(filename):
				print >>sys.stderr,"%s is not a filename,please check it" %filename
				continue
			if not os.path.exists(filename):
				print >>sys.stderr,"%s is not exists,please your input" %filename
				continue
			data = open(filename).read()
			charts,words,lines = get_count(data)
			t_charts += charts
			t_words += words
			t_lines += lines
			need_print(p,charts,words,lines,filename)

		if len(args) > 1:
			if p.nototal == False:
				need_print(p,t_charts,t_words,t_lines,"Total")
	else:
		data = sys.stdin.read()
		charts,words,lines = get_count(data)
		if p.nototal == True:
			print >>sys.stderr,"If there is no filename,you can't use this argvment!"
		else:
			need_print(p,charts,words,lines,"Total")


