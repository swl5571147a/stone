#!/usr/bin/evn python
import time
from optparse import OptionParser
import sys
import os

def get_count(data):
	charts = len(data)
	words = len(data.split())
	lines = data.count("\n")

	return charts,words,lines

parser = OptionParser(usage = "%prog [-c] [-w] [-l] [-h] can be used")
parser.add_option('-c','--chart',dest='chart',action='store_true',default=False,help='count charts')
parser.add_option('-w','--word',dest='word',action='store_true',default=False,help='count words')
parser.add_option('-l','--line',dest='line',action='store_true',default=False,help='count lines')

p, args = parser.parse_args()

if not (p.chart or p.word or p.line):
	p.chart,p.word,p.line = True,True,True

if len(args) > 0:
	t_charts,t_words,t_lines = 0,0,0
	for filename in args:
		if os.path.isdir(filename) or os.path.islink(filename):
			print >>sys.stderr,"%s is a dir,please enter filename" %filename
			continue
		else:
			if not os.path.exists(filename):
				print >>sys.stderr,"%s is not exists,please check it" %filename
				continue
		data = open(filename).read()
		charts,words,lines = get_count(data)
		t_charts += charts
		t_words += words
		t_lines += lines
		if p.chart == True:
			print "charts:%s"%charts,
		if p.word == True:
			print "words:%s"%words,
		if p.line == True:
			print "lines:%s"%lines,
		print filename

	if len(args) > 1:		
		if p.chart == True:
			print "charts count:%s" %t_charts,
		if p.word == True:
			print "words count:%s" %t_words,
		if p.line == True:
			print "lines count:%s" %t_lines,
		print "Total"
else:
	data = sys.stdin.read()
	charts,words,lines = get_count(data)
	if p.chart == True:
		print "charts:%s" %charts,
	if p.word == True:
		print "words:%s" %words,
	if p.line == True:
		print "lines:%s" %lines,
	print "Total"
