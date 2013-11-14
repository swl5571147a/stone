#!/usr/bin/env python
#coding:utf-8

import httplib

def check_web_server(host,port,path):
	h = httplib.HTTPConnection(host,port)
	h.request('GET',path)
	resp = h.getresponse()
	print 'HTTP Response:'
	print '\tstatus=',resp.status
	print '\treason=',resp.reason
	print 'HTTP Headers:'
	for hdr in resp.getheaders():
		print '\t%s:%s' %hdr
	print type(resp.getheaders())
	print resp.getheaders()

check_web_server('www.baidu.com',80,'/')
