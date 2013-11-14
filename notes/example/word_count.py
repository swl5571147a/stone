#!/usr/bin/python 
#coding:utf-8

import sys

input = sys.stdin

def WrodCount(f):
	n = 0
	for i in f:
		n += 1
	return n

print WrodCount(input)
