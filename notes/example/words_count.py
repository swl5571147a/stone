#!/usr/bin/env python
#coding:utf-8

import sys

data = sys.stdin.read()
charts = len(data)
words = len(data.split())
lines = data.count("\n")

print "字符共计：%(charts)s   字数共计：%(words)s   行数共计：%(lines)s" %locals()
